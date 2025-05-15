import os
import asyncio
import requests
from telethon import TelegramClient
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import UserStatusOnline

# Zmienne środowiskowe
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
chat_id = int(os.getenv("CHAT_ID"))
user_to_track = os.getenv("USER_TO_TRACK")  # może być username bez @ lub user_id jako string/liczba

print("==> Startuję bota...")

client = TelegramClient("bot_session", api_id, api_hash)

async def main():
    await client.start(bot_token=bot_token)
    print("==> Bot zalogowany jako bot i gotowy.")
    await client.send_message(chat_id, "Bot uruchomiony!")

    was_online = False

    while True:
        try:
            user = await client.get_entity(user_to_track)
            full = await client(GetFullUserRequest(user.id))
            status = full.user.status

            if isinstance(status, UserStatusOnline) and not was_online:
                message = f"{user.first_name} jest ONLINE!"
                print("==>", message)
                requests.post(
                    f"https://api.telegram.org/bot{bot_token}/sendMessage",
                    data={'chat_id': chat_id, 'text': message}
                )
                was_online = True

            elif not isinstance(status, UserStatusOnline):
                was_online = False

        except Exception as e:
            print("Błąd podczas sprawdzania statusu:", e)

        await asyncio.sleep(10)

asyncio.run(main())
