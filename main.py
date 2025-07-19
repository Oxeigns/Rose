import os
from pyrogram import Client
from handlers import register_all

API_ID = int(os.environ.get('API_ID', '12345'))
API_HASH = os.environ.get('API_HASH', '')
BOT_TOKEN = os.environ.get('BOT_TOKEN', '')

app = Client('rose_bot', api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

register_all(app)

if __name__ == '__main__':
    print('Starting bot...')
    app.run()
