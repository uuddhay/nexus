"""Skill curator — background task that maintains the skill library.

Runs as a scheduled action. Responsibilities:
1. Merge duplicate skills (similar names, overlapping procedures)
2. Archive stale skills (not used in N days, low confidence)
3. Boost confidence for skills with repeated successful use
"""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timezone
from typing import List, Optional

from services.memory.skills import SkillsManager
from services.memory.skill_format import Skill

logger = logging.getLogger(__name__)

# Days without use before a skill is considered stale
STALE_AFTER_DAYS = 90

# Confidence threshold for auto-archiving
ARCHIVE_CONFIDENCE_THRESHOLD = 0.2

# Minimum uses before confidence can be boosted
BOOST_MIN_USES = 3

# Confidence boost per use (up to max)
BOOST_PER_USE = 0.05
BOOST_MAX_CONFIDENCE = 0.95


async def run_curator(owner: str, data_dir: str) -> str:
    """Run one full curator pass for the given owner.

    Returns a human-readable summary of what was done.
    """
    sm = SkillsManager(data_dir)
    skills = sm.load(owner=owner)
    if not skills:
        return "No skills to curate."

    reports = []
    duplicates = _find_duplicates(skills)
    if duplicates:
        for group in duplicates:
            keeper, to_merge = group[0], group[1:]
            merged = await _merge_skills(keeper, to_merge, sm, owner)
            if merged:
                reports.append(f"Merged {len(to_merge)} skill(s) into '{keeper.get('name', '?')}'")

    stale = _find_stale(skills)
    for s in stale:
        try:
            sm.set_status(owner, s.get("name", ""), "archived")
            reports.append(f"Archived stale skill '{s.get('name', '?')}'")
        except Exception as e:
            logger.warning("curator: failed to archive '%s': %s", s.get("name"), e)

    boosted = _boost_confidence(skills, sm, owner)
    for name, new_conf in boosted:
        reports.append(f"Boosted confidence for '{name}' to {new_conf:.2f}")

    # Write the report as a note
    if reports:
        summary = "## Curator Report\n\n" + "\n".join(f"- {r}" for r in reports)
        try:
            from core.database import SessionLocal as DB, Note
            now = datetime.now(timezone.utc).replace(tzinfo=None)
            note = Note(
                id=os.urandom(4).hex(),
                owner=owner,
                title=f"Skill Curator — {datetime.now().strftime('%Y-%m-%d')}",
                content=summary,
                note_type="markdown",
                created_at=now,
                updated_at=now,
            )
            db = DB()
            try:
                db.add(note)
                db.commit()
            finally:
                db.close()
        except Exception as e:
            logger.warning("curator: failed to save report note: %s", e)

    return "\n".join(reports) if reports else "No curation needed."


def _find_duplicates(skills: List[Skill]) -> List[List[Skill]]:
    """Find groups of skills that may be duplicates.

    Uses Jaccard similarity on skill names and descriptions.
    Returns groups where the first item is the keeper and the rest are candidates
    for merging.
    """
    groups = []
    checked = set()

    for i, a in enumerate(skills):
        if i in checked:
            continue
        a_name = (a.get("name") or "").lower()
        a_desc = (a.get("description") or "").lower()
        a_tokens = set(a_name.split("-")) | set(a_desc.split())

        group = [a]
        checked.add(i)

        for j, b in enumerate(skills):
            if j in checked or i == j:
                continue
            b_name = (b.get("name") or "").lower()
            b_desc = (b.get("description") or "").lower()
            b_tokens = set(b_name.split("-")) | set(b_desc.split())

            # Jaccard similarity on token sets
            if not a_tokens or not b_tokens:
                continue
            similarity = len(a_tokens & b_tokens) / len(a_tokens | b_tokens)
            if similarity > 0.5:
                group.append(b)
                checked.add(j)

        if len(group) > 1:
            # Sort by confidence — highest first is the keeper
            group.sort(key=lambda s: _confidence(s), reverse=True)
            groups.append(group)

    return groups


async def _merge_skills(
    keeper: Skill,
    to_merge: List[Skill],
    sm: SkillsManager,
    owner: str,
) -> bool:
    """Merge skills into the keeper. Combines procedures, pitfalls, and
    verification sections. Archives the merged-away skills.
    """
    try:
        keeper_body = keeper.get("body") or ""
        keeper_name = keeper.get("name", "unknown")

        for merge_skill in to_merge:
            merge_body = merge_skill.get("body") or ""
            merge_name = merge_skill.get("name", "")

            if merge_body and merge_body not in keeper_body:
                # Append unique content from the merge skill
                keeper_body += f"\n\n---\n*Merged from {merge_name}*\n\n{merge_body}"

            # Archive the merged skill
            try:
                sm.set_status(owner, merge_name, "archived")
            except Exception:
                pass

        sm.update(owner, keeper_name, body=keeper_body)
        return True
    except Exception as e:
        logger.warning("curator: merge failed: %s", e)
        return False


def _find_stale(skills: List[Skill]) -> List[Skill]:
    """Find skills that are stale (unused for STALE_AFTER_DAYS and low confidence)."""
    now = datetime.now(timezone.utc).timestamp()
    stale = []
    for s in skills:
        if s.get("status") == "archived":
            continue
        if _confidence(s) < ARCHIVE_CONFIDENCE_THRESHOLD:
            stale.append(s)
            continue
        last_used = s.get("last_used") or s.get("created")
        if last_used:
            try:
                if isinstance(last_used, str):
                    last_ts = datetime.fromisoformat(last_used.replace("Z", "+00:00")).timestamp()
                else:
                    last_ts = float(last_used)
                if (now - last_ts) > STALE_AFTER_DAYS * 86400:
                    stale.append(s)
            except (ValueError, TypeError):
                pass
    return stale


def _boost_confidence(skills: List[Skill], sm: SkillsManager, owner: str) -> List[tuple]:
    """Boost confidence for skills used repeatedly with success."""
    boosted = []
    for s in skills:
        uses = s.get("uses", 0) if isinstance(s.get("uses"), (int, float)) else 0
        if uses >= BOOST_MIN_USES:
            current_conf = _confidence(s)
            if current_conf < BOOST_MAX_CONFIDENCE:
                new_conf = min(current_conf + BOOST_PER_USE * uses, BOOST_MAX_CONFIDENCE)
                try:
                    sm.set_confidence(owner, s.get("name", ""), new_conf)
                    boosted.append((s.get("name", "?"), new_conf))
                except Exception as e:
                    logger.warning("curator: confidence boost failed: %s", e)
    return boosted


def _confidence(skill: Skill) -> float:
    try:
        return float(skill.get("confidence", 0) or 0)
    except (TypeError, ValueError):
        return 0.0
