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

    @client.on(events.NewMessage(from_users=user_id_to_track))
    async def handle_message(event):
        print(f"==> Wiadomość od {user_to_track}: {event.text}")
        await client.send_message(chat_id, f"{user_to_track} napisał:\n{event.text}")

    await client.run_until_disconnected()

# Uruchomienie
client.loop.run_until_complete(main())
