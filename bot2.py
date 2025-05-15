import asyncio
from telethon import TelegramClient
from telethon.tl.types import UserStatusOnline
import requests
import time

api_id = 20375615
api_hash = 'a42c3d95a903f070a77dc8fdea40a6e4'
bot_token = '7571531890:AAEZkeQNUrK4MhowVPdOPVCiXV0Nh6w2RKc'
chat_id = 7029563819
user_id_to_track = 5000291224

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

with client:
    client.loop.run_until_complete(main())
