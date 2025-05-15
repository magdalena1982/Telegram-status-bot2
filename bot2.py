import os
import base64

session_file = 'session_name.session'

if not os.path.exists(session_file):
    encoded = os.getenv('SESSION_BASE64')
    if encoded:
        with open(session_file, 'wb') as f:
            f.write(base64.b64decode(encoded))
    else:
        print("Brak zmiennej SESSION_BASE64!")


import os
import asyncio
from telethon import TelegramClient
from telethon.tl.types import UserStatusOnline

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
chat_id = int(os.getenv("CHAT_ID"))
user_to_track = os.getenv("USER_TO_TRACK")

client = TelegramClient('user_session', api_id, api_hash)

async def main():
    await client.start()
    print("==> Bot zalogowany jako użytkownik i gotowy.")
    
    was_online = False
    
    while True:
        user = await client.get_entity(user_to_track)
        status = user.status
        
        if isinstance(status, UserStatusOnline) and not was_online:
            msg = f"{user.first_name} jest ONLINE!"
            await client.send_message(chat_id, msg)
            was_online = True
            print(msg)
        elif not isinstance(status, UserStatusOnline):
            was_online = False
        
        await asyncio.sleep(10)  # sprawdzaj co 60 sekund

asyncio.run(main())
