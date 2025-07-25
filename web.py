"""Minimal Flask app used when running the bot as a web service."""

from flask import Flask, request
import logging
import os

LOGGER = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def index():
    return 'Rose bot is running.'


@app.post('/webhook')
def webhook():
    """Endpoint for Telegram webhooks. Only logs the payload for now."""
    LOGGER.debug('Webhook payload: %s', request.json)
    return 'ok'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
