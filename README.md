# Rose Telegram Bot

This repository contains the source code for **Rose**, a modular Telegram bot built with [Pyrogram](https://github.com/pyrogram/pyrogram). The bot uses a small SQLite database and is designed to be easily deployable to platforms such as Heroku or Render.

## Features
- Modular handler architecture
- SQLite storage
- Example configuration via `.env.example`
- Extensive debug logging for easier troubleshooting

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
   All logs are output at the DEBUG level for easy diagnostics.

## Deployment
Example files are provided for running on container platforms:
- `Dockerfile` for Docker based deployments
- `Procfile` and `render.yaml` for hosting services

## Telegram Setup
1. Disable privacy mode for your bot via **BotFather** so it can see all group
   messages.
2. Add the bot to your group and promote it to **admin** with permission to
   delete messages and restrict users. Most features require admin rights.
3. Use `/start` or `/help` to verify the bot responds. Inline buttons rely on
   callback queries which are registered automatically when the bot starts.

---
Licensed under the MIT License.
