#!/usr/bin/env bash
set -e

# Activate virtual environment when available
if [ -d "venv" ]; then
  source venv/bin/activate
fi

# Ensure DEPLOY_MODE defaults to worker so long polling works on services like Render
export DEPLOY_MODE="${DEPLOY_MODE:-worker}"

exec python -u main.py
