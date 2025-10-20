import os
import time
from telethon import TelegramClient, events, Button
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
TARGET_CHANNEL = os.getenv("TARGET_CHANNEL")

bot = TelegramClient("button_adder", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# === Anti duplikat ===
recent_messages = {}
TIMEOUT = 5  # detik

@bot.on(events.NewMessage)
async def handler(event):
    try:
        # Identifikasi unik pesan (chat_id + message_id)
        key = f"{event.chat_id}:{event.id}"
        now = time.time()

        # Abaikan jika pesan baru saja diproses
        if key in recent_messages and now - recent_messages[key] < TIMEOUT:
            print(f"⚠️ Duplikat abaikan pesan {event.id}")
            return

        recent_messages[key] = now

        # Abaikan jika pesan dari channel atau group
        if event.is_channel or event.is_group:
            return

        # Tambahkan tombol
        buttons = [[Button.url("📢Channel Backup", "https://t.me/+cVbvBt4YtAk1ODI1")]]

        # Kirim ke target
        await bot.send_message(
            TARGET_CHANNEL,
            event.message,
            buttons=buttons,
            link_preview=False
        )

        print(f"✅ Pesan {event.id} dikirim ke {TARGET_CHANNEL}")

    except Exception as e:
        print(f"❌ Error: {e}")

print("🤖 Button Adder Bot aktif! Menunggu pesan dari akun forwarder...")
bot.run_until_disconnected()
