#!/usr/bin/env bash
set -e

# Activate virtual environment when available
if [ -d "venv" ]; then
  source venv/bin/activate
fi

python main.py
