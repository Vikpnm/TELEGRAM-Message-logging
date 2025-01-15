import os
import datetime
from telethon import TelegramClient, events
from telethon.tl.functions.account import UpdateStatusRequest
from asyncio import sleep
import config  # Импорт файла с API-ключами

# Название сессии
session_name = 'always_online_bot'

# Создаем папку для логов, если ее нет
os.makedirs('logs', exist_ok=True)

# Инициализация клиента с использованием ключей из config.py
client = TelegramClient(session_name, config.api_id, config.api_hash)

# Функция для поддержания статуса "онлайн"
async def stay_online():
    while True:
        try:
            # Обновляем статус
            await client(UpdateStatusRequest(online=True))
            print(f"[{datetime.datetime.now()}] Статус 'онлайн' обновлен.")
        except Exception as e:
            print(f"Ошибка обновления статуса: {e}")
        # Ждем 5 минут перед следующим обновлением статуса
        await sleep(300)

# Обработка новых сообщений
@client.on(events.NewMessage)
async def handle_new_message(event):
    # Проверяем, что сообщение пришло из личного чата
    if event.is_private:
        sender = await event.get_sender()  # Получаем отправителя
        sender_name = sender.username if sender.username else sender.first_name
        message = event.message.message

        # Логирование сообщения
        log_message = f"[{datetime.datetime.now()}] {sender_name}: {message}\n"
        with open('logs/messages.log', 'a', encoding='utf-8') as f:
            f.write(log_message)
        print(log_message)  # Для наглядности выводим в консоль

# Запуск клиента
async def main():
    # Запускаем задачу для поддержания статуса "онлайн"
    client.loop.create_task(stay_online())
    # Запускаем клиента
    await client.start()
    print("Бот запущен и слушает новые сообщения.")
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
