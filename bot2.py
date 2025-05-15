import asyncio
import os
from telethon import TelegramClient
from telethon.tl.types import UserStatusOnline
import requests
from dotenv import load_dotenv

load_dotenv()  # Ładuje zmienne z .env w trakcie lokalnych testów

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
chat_id = int(os.getenv("CHAT_ID"))
user_to_track = os.getenv("USER_TO_TRACK")  # username (bez @) lub ID jako tekst

was_online = False

client = TelegramClient('bot', api_id, api_hash)

async def main():
    await client.start(bot_token=bot_token)
    print("Bot uruchomiony. Czekam na status online...")

    global was_online

    try:
        user = await client.get_entity(user_to_track)
    except ValueError:
        print(f"Nie udało się znaleźć użytkownika: {user_to_track}. Sprawdź, czy bot ma z nim kontakt.")
        return

    while True:
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
