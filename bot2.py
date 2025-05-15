import os
import asyncio
from telethon import TelegramClient
from telethon.tl.types import UserStatusOnline
import requests

api_id = int(os.getenv('API_ID'))  # zdefiniuj zmienną API_ID w Render
api_hash = os.getenv('API_HASH')   # zdefiniuj zmienną API_HASH w Render
bot_token = os.getenv('BOT_TOKEN') # zdefiniuj zmienną BOT_TOKEN w Render
chat_id = int(os.getenv('CHAT_ID'))  # również możesz zrobić chat_id zmienną środowiskową
user_id_to_track = int(os.getenv('USER_ID_TO_TRACK'))  # i user_id_to_track

was_online = False

client = TelegramClient('bot', api_id, api_hash)

async def main():
    await client.start(bot_token=bot_token)
    print("Bot uruchomiony. Czekam na status online...")

    global was_online

    while True:
        user = await client.get_entity(user_id_to_track)
        status = user.status

        if isinstance(status, UserStatusOnline) and not was_online:
            message = f"{user.first_name} jest ONLINE!"
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            requests.post(url, data={'chat_id': chat_id, 'text': message})
            was_online = True

        if not isinstance(status, UserStatusOnline):
            was_online = False

        await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())
