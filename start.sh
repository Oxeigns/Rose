#!/usr/bin/env bash

# Activate virtual environment if exists
if [ -d "venv" ]; then
  source venv/bin/activate
fi

python main.py
