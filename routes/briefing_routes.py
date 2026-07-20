"""Morning Briefing — opt-in, configurable, auto-scheduled daily brief.

API:
  GET  /api/briefing/config     — get current briefing config
  PUT  /api/briefing/config     — set briefing config + auto-schedule/unschedule
  POST /api/briefing/trigger    — manually trigger the brief now

Config (stored in user prefs):
  {
    "enabled": false,           // opt-in — off by default
    "time": "07:00",           // HH:MM
    "include_calendar": true,
    "include_email": true,
    "include_todos": true,
    "include_research": false,  // requires Deep Research
    "delivery": "note",         // "note" | "email"
    "research_topics": []       // optional topics for Deep Research
  }
"""

from __future__ import annotations

import json
import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, Request

from core.database import SessionLocal, ScheduledTask
from src.auth_helpers import get_current_user
from routes.prefs_routes import _load_for_user, _save_for_user

logger = logging.getLogger(__name__)

BRIEFING_PREFS_KEY = "morning_briefing"

DEFAULT_CONFIG = {
    "enabled": False,
    "time": "07:00",
    "include_calendar": True,
    "include_email": True,
    "include_todos": True,
    "include_research": False,
    "delivery": "note",
    "research_topics": [],
    "curator_enabled": False,       # auto-curate skills weekly
    "curator_day": "mon",           # day of week for curator
    "curator_time": "03:00",        # HH:MM
}


def _get_briefing_config(user: str) -> dict:
    """Load briefing config from user prefs, merging with defaults."""
    prefs = _load_for_user(user)
    stored = prefs.get(BRIEFING_PREFS_KEY, {})
    if isinstance(stored, dict):
        return {**DEFAULT_CONFIG, **stored}
    return dict(DEFAULT_CONFIG)


def _save_briefing_config(user: str, config: dict):
    """Save briefing config to user prefs."""
    prefs = _load_for_user(user)
    merged = {**DEFAULT_CONFIG, **(prefs.get(BRIEFING_PREFS_KEY, {}) or {}), **config}
    prefs[BRIEFING_PREFS_KEY] = merged
    _save_for_user(user, prefs)


def _sync_briefing_task(user: str, config: dict):
    """Create or delete the scheduled daily_brief task based on config."""
    db = SessionLocal()
    try:
        # Look for existing briefing task
        task = db.query(ScheduledTask).filter(
            ScheduledTask.owner == user,
            ScheduledTask.action == "daily_brief",
        ).first()

        if not config.get("enabled"):
            # Remove task if exists
            if task:
                db.delete(task)
                db.commit()
                logger.info("briefing: removed scheduled task for %s", user)
        else:
            time_str = config.get("time", "07:00")
            try:
                hour, minute = time_str.split(":")
                hour = int(hour)
                minute = int(minute)
            except (ValueError, TypeError):
                hour, minute = 7, 0

            prompt_data = {
                "include_calendar": config.get("include_calendar", True),
                "include_email": config.get("include_email", True),
                "include_todos": config.get("include_todos", True),
                "include_research": config.get("include_research", False),
                "delivery": config.get("delivery", "note"),
                "research_topics": config.get("research_topics", []),
            }

            if task:
                task.scheduled_time = f"{hour:02d}:{minute:02d}"
                task.prompt = json.dumps(prompt_data)
                task.is_active = True
                db.commit()
                logger.info("briefing: updated scheduled task for %s", user)
            else:
                new_task = ScheduledTask(
                    id=str(uuid.uuid4())[:8],
                    owner=user,
                    name="Morning Briefing",
                    action="daily_brief",
                    task_type="action",
                    schedule="daily",
                    scheduled_time=f"{hour:02d}:{minute:02d}",
                    prompt=json.dumps(prompt_data),
                    output_target="note",
                    is_active=True,
                )
                db.add(new_task)
                db.commit()
                logger.info("briefing: created scheduled task for %s at %s", user, time_str)

        # ── Curator task ──
        curator_enabled = config.get("curator_enabled", False)
        curator_task = db.query(ScheduledTask).filter(
            ScheduledTask.owner == user,
            ScheduledTask.action == "curate_skills",
        ).first()

        if not curator_enabled:
            if curator_task:
                db.delete(curator_task)
                db.commit()
                logger.info("briefing: removed curator task for %s", user)
        else:
            c_day = config.get("curator_day", "mon")
            c_time = config.get("curator_time", "03:00")
            day_map = {"mon": 0, "tue": 1, "wed": 2, "thu": 3, "fri": 4, "sat": 5, "sun": 6}
            c_dow = day_map.get(c_day, 0)

            if curator_task:
                curator_task.scheduled_time = c_time
                curator_task.scheduled_day = c_dow
                curator_task.is_active = True
                db.commit()
            else:
                new_task = ScheduledTask(
                    id=str(uuid.uuid4())[:8],
                    owner=user,
                    name="Skill Curator",
                    action="curate_skills",
                    task_type="action",
                    schedule="weekly",
                    scheduled_time=c_time,
                    scheduled_day=c_dow,
                    output_target="note",
                    is_active=True,
                )
                db.add(new_task)
                db.commit()
                logger.info("briefing: created curator task for %s on %s at %s", user, c_day, c_time)
    finally:
        db.close()


# Avoid circular import at module level
import uuid  # noqa: E402


def setup_briefing_routes():
    router = APIRouter(prefix="/api/briefing", tags=["briefing"])

    @router.get("/config")
    async def get_config(request: Request):
        user = get_current_user(request)
        return _get_briefing_config(user)

    @router.put("/config")
    async def set_config(request: Request, body: dict):
        user = get_current_user(request)
        if not user:
            raise HTTPException(status_code=401, detail="Not authenticated")

        config = _get_briefing_config(user)
        # Merge only known keys
        for key in DEFAULT_CONFIG:
            if key in body:
                config[key] = body[key]

        _save_briefing_config(user, config)
        _sync_briefing_task(user, config)
        return config

    @router.post("/trigger")
    async def trigger_now(request: Request):
        """Manually trigger the briefing right now."""
        user = get_current_user(request)
        if not user:
            raise HTTPException(status_code=401, detail="Not authenticated")

        from src.builtin_actions import action_daily_brief
        from datetime import datetime

        logger.info("briefing: manual trigger for %s", user)
        try:
            message, ok = await action_daily_brief(owner=user)
            return {"success": ok, "message": message, "triggered_at": datetime.utcnow().isoformat()}
        except Exception as e:
            logger.error("briefing: manual trigger failed: %s", e)
            raise HTTPException(status_code=500, detail=str(e))

    return router
