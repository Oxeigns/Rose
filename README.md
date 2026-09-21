# Rose Telegram Bot

This repository contains the source code for **Rose**, a modular Telegram bot built with [Pyrogram](https://github.com/pyrogram/pyrogram). The bot uses a small SQLite database and is designed to be easily deployable to platforms such as Heroku or Render.

## Features
- Modular handler architecture
- SQLite storage
- Example configuration via `.env.example`
- Informative logging by default for easier monitoring

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
     All logs are output at the INFO level by default.

Set `DEPLOY_MODE=worker` for a background worker. For a web service,
`DEPLOY_MODE=webhook` is retained as a legacy setting that starts an HTTP
health endpoint on `0.0.0.0:$PORT`. Telegram updates still arrive through
Pyrogram's MTProto connection. `WEBHOOK_URL` is not required and Bot API
webhook payloads are not accepted by this service.

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
