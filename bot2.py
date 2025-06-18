import os
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.types import UserStatusOnline
from telethon.errors import AuthKeyDuplicatedError

# Dane logowania
api_id = int(os.getenv("API_ID2"))
api_hash = os.getenv("API_HASH2")
session_string = os.getenv("SESSION_STRING2")
chat_id = int(os.getenv("CHAT_ID2"))
user_to_track = os.getenv("USER_TO_TRACK")

# Tworzenie klienta z StringSession
client = TelegramClient(StringSession(session_string), api_id, api_hash)

async def main():
    try:
        await client.start()
        print("==> Bot zalogowany jako użytkownik i gotowy.")
    except AuthKeyDuplicatedError:
        print("❌ Błąd: sesja została użyta z różnych IP. Zrestartuj sesję.")
        return
    
    was_online = False

    while True:
        try:
            user = await client.get_entity(user_to_track)
            status = user.status

            if isinstance(status, UserStatusOnline) and not was_online:
                msg = f"{user.first_name} jest ONLINE!"
                await client.send_message(chat_id, msg)
                was_online = True
                print(msg)
            elif not isinstance(status, UserStatusOnline):
                was_online = False

            await asyncio.sleep(1)  # Możesz zmienić na 60, jeśli chcesz rzadziej sprawdzać
        except Exception as e:
            print(f"Błąd: {e}")
            await asyncio.sleep(5)  # Odczekaj chwilę i spróbuj dalej

asyncio.run(main())
