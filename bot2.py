import asyncio
import os
from telethon import TelegramClient
from telethon.tl.types import UserStatusOnline
import requests
import sys

# Wczytanie zmiennych środowiskowych
try:
    api_id = int(os.getenv("API_ID"))
    api_hash = os.getenv("API_HASH")
    bot_token = os.getenv("BOT_TOKEN")
    chat_id = int(os.getenv("CHAT_ID"))
    user_to_track = os.getenv("USER_TO_TRACK")

    if not all([api_id, api_hash, bot_token, chat_id, user_to_track]):
        raise ValueError("Brakuje jednej lub więcej zmiennych środowiskowych.")
except Exception as e:
    print(f"Błąd przy wczytywaniu zmiennych: {e}")
    sys.exit(1)

was_online = False
client = TelegramClient('bot', api_id, api_hash)

async def main():
    await client.start(bot_token=bot_token)
    print("Bot uruchomiony. Czekam na status online...")

    global was_online

    try:
        user = await client.get_entity(user_to_track)
        print(f"Śledzony użytkownik: {user.first_name} (id: {user.id})")
    except Exception as e:
        print(f"Błąd przy pobieraniu użytkownika '{user_to_track}': {e}")
        return

    while True:
        try:
            status = user.status

            if isinstance(status, UserStatusOnline) and not was_online:
                message = f"{user.first_name} jest ONLINE!"
                print(message)
                url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
                requests.post(url, data={'chat_id': chat_id, 'text': message})
                was_online = True

            if not isinstance(status, UserStatusOnline):
                was_online = False

        except Exception as e:
            print(f"Błąd w pętli sprawdzania statusu: {e}")

        await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())
