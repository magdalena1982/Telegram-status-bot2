import os
import asyncio
from telethon import TelegramClient, events

# Zmienne środowiskowe
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
chat_id = int(os.getenv("CHAT_ID"))
user_id_to_track = int(os.getenv("USER_ID_TO_TRACK"))
user_to_track = os.getenv("USER_TO_TRACK")

print("==> Startuję bota...")

# Tworzenie klienta z tokenem bota
client = TelegramClient('bot_session', api_id, api_hash)

async def main():
    await client.start(bot_token=bot_token)
    print("==> Bot zalogowany jako bot i gotowy.")
    await client.send_message(chat_id, "Bot uruchomiony!")

was_online = False

    while True:
        user = client.get_entity(user_id_to_track)
        user_info = client.get_peer_id(user)
        status = user.status

        if isinstance(status, UserStatusOnline) and not was_online:
            # Wyślij powiadomienie przez bota
            message = f"{user.first_name} jest ONLINE!"
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            requests.post(url, data={'chat_id': chat_id, 'text': message})
            was_online = True

        if not isinstance(status, UserStatusOnline):
            was_online = False

        time.sleep(60)  # sprawdza co 60 sekund

# Uruchomienie
asyncio.run(main())
