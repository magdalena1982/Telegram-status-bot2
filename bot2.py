import os
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.types import UserStatusOnline
from telethon.errors import AuthKeyDuplicatedError

api_id = int(os.getenv("API_ID2"))
api_hash = os.getenv("API_HASH2")
session_string = os.getenv("SESSION2_BASE64")  # tak, jak masz u siebie
chat_id = int(os.getenv("CHAT_ID2"))
user_to_track = os.getenv("USER_TO_TRACK")

client = TelegramClient(StringSession(session_string), api_id, api_hash)

async def main():
    try:
        await client.connect()
        if not await client.is_user_authorized():
            print("❌ Sesja nieważna. Wygeneruj SESSION2_BASE64 ponownie.")
            return

        print("✅ Bot zalogowany.")

        was_online = False
        while True:
            try:
                user = await client.get_entity(user_to_track)
                status = user.status

                if isinstance(status, UserStatusOnline) and not was_online:
                    msg = f"{user.first_name} (@{user.username}) jest ONLINE!"
                    await client.send_message(chat_id, msg)
                    was_online = True
                    print(msg)
                elif not isinstance(status, UserStatusOnline):
                    was_online = False

                await asyncio.sleep(1)
            except Exception as e:
                print(f"❌ Błąd w pętli: {e}")
                await asyncio.sleep(5)
    except AuthKeyDuplicatedError:
        print("❌ Sesja używana na innym IP. Zresetuj sesję.")
    finally:
        await client.disconnect()
        print("Klient rozłączony.")

if __name__ == "__main__":
    asyncio.run(main())
