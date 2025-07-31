import importlib
import pkgutil
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN

app = Client(
    "referbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins={"root": "plugins"}
)

for _, module_name, _ in pkgutil.iter_modules(['plugins']):
    importlib.import_module(f'plugins.{module_name}')

if __name__ == '__main__':
    print("Bot Started")
    app.run()
