from telethon.sync import TelegramClient
from telethon.tl.types import UserStatusOnline
import requests
import time

api_id = 20375615  # wpisz swój
api_hash = 'a42c3d95a903f070a77dc8fdea40a6e4'
bot_token = '7571531890:AAEZkeQNUrK4MhowVPdOPVCiXV0Nh6w2RKc'
chat_id = 7029563819 # ID Twojego czatu (możemy zdobyć)
user_id_to_track = 5000291224  # ID osoby, którą chcesz śledzić

was_online = False

with TelegramClient('session_name', api_id, api_hash) as client:
    print("Bot uruchomiony. Czekam na status online...")
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

        time.sleep(10)  # sprawdza co 10 sekund
