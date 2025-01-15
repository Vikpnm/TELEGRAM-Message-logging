import os
import datetime
from telethon import TelegramClient, events
import config

session_name = 'message_logger_bot'

os.makedirs('logs', exist_ok=True)
client = TelegramClient(session_name, config.api_id, config.api_hash)
@client.on(events.NewMessage)
async def handle_new_message(event):
    if event.is_private:
        sender = await event.get_sender()
        sender_name = sender.username if sender.username else sender.first_name
        message = event.message.message

        log_message = f"[{datetime.datetime.now()}] {sender_name}: {message}\n"
        with open('logs/messages.log', 'a', encoding='utf-8') as f:
            f.write(log_message)
        print(log_message)

async def main():
    await client.start()
    print("BOT has been started...")
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
