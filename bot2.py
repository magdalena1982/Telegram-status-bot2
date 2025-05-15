import os
import asyncio
from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError

# Wczytanie zmiennych środowiskowych
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
chat_id = int(os.getenv("CHAT_ID"))
user_id_to_track = int(os.getenv("USER_ID_TO_TRACK"))
user_to_track = os.getenv("USER_TO_TRACK")

print("==> Startuję bota...")

# Tworzenie klienta
client = TelegramClient('bot_session', api_id, api_hash)

async def main():
    try:
        await client.start(bot_token=bot_token)
        print("==> Bot wystartował i jest online.")
        await client.send_message(chat_id, "Bot został uruchomiony na Render!")

        # Nasłuchiwanie wiadomości od śledzonego użytkownika
        @client.on(events.NewMessage(from_users=user_id_to_track))
        async def handler(event):
            print(f"==> Nowa wiadomość od {user_id_to_track}: {event.text}")
            await client.send_message(chat_id, f"Użytkownik {user_to_track} napisał: {event.text}")

        await client.run_until_disconnected()

    except SessionPasswordNeededError:
        print("==> Potrzebne hasło dwuskładnikowe (2FA), a bot go nie obsługuje.")
    except Exception as e:
        print(f"==> Błąd krytyczny: {e}")
        try:
            await client.send_message(chat_id, f"Błąd bota: {e}")
        except:
            print("==> Nie można wysłać wiadomości o błędzie do Telegrama.")

# Uruchomienie
with client:
    client.loop.run_until_complete(main())
