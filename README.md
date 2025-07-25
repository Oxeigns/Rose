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

Set `DEPLOY_MODE=worker` to run the bot with long polling. When deploying as a
web service you can use `DEPLOY_MODE=webhook` together with `WEBHOOK_URL` and
`PORT` so the FastAPI server listens on `0.0.0.0:$PORT` and Telegram can reach
your endpoint.

When deploying to **Render**, make sure the service is a **worker** so the bot
polls Telegram for updates. The provided `render-worker.yaml` blueprint sets the
correct command and environment variables out of the box.

## Deployment
Example files are provided for running on container platforms:
- `Dockerfile` for Docker based deployments
- `Procfile` for Heroku style platforms
- `render.yaml` for a combined worker/webhook setup on Render
- `render-worker.yaml` and `render-webhook.yaml` demonstrate separate services
  for long polling and webhook modes on Render

---
Licensed under the MIT License.
