# Rose Telegram Bot

This repository contains the source code for **Rose**, a modular Telegram bot built with [Pyrogram](https://github.com/pyrogram/pyrogram). The bot uses a small SQLite database and is designed to be easily deployable to platforms such as Heroku or Render.

## Features
- Modular handler architecture
- SQLite storage
- Example configuration via `.env.example`

## Running locally
1. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```
2. Copy `.env.example` to `.env` and fill in your credentials.
3. Start the bot:
   ```bash
   python main.py
   ```
   The bot will exit with an error message if any required credential is missing.

## Deployment
Example files are provided for running on container platforms:
- `Dockerfile` for Docker based deployments
- `Procfile` and `render.yaml` for hosting services

---
Licensed under the MIT License.
