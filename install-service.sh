#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVICE_FILE="$SCRIPT_DIR/nexus-ui.service"

if [ ! -f "$SERVICE_FILE" ]; then
  echo "Error: nexus-ui.service not found in $SCRIPT_DIR"
  exit 1
fi

echo "Installing Nexus UI service..."
echo "Make sure you've edited nexus-ui.service with your username and paths first!"
echo ""

sudo cp "$SERVICE_FILE" /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable nexus-ui
sudo systemctl start nexus-ui
sudo systemctl status nexus-ui
