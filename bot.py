from pyrogram import Client, filters
import asyncio, re, os

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

app = Client("my_account", api_id=API_ID, api_hash=API_HASH)
tasks = {}

async def send_loop(chat, text, interval):
    while True:
        await app.send_message(chat, text)
        await asyncio.sleep(interval * 60)

@app.on_message(filters.me & filters.regex(r"^s\.\s(.+)\s(@\S+)\s(\d+)$"))
async def start_spam(client, message):
    text, chat, minutes = re.match(r"^s\.\s(.+)\s(@\S+)\s(\d+)$", message.text).groups()
    minutes = int(minutes)
    if chat in tasks:
        await message.reply("уже запущен для этого чата.")
        return
    task = asyncio.create_task(send_loop(chat, text, minutes))
    tasks[chat] = task
    await message.reply(f"запущено: '{text}' -> {chat} каждые {minutes} мин.")

@app.on_message(filters.me & filters.regex(r"^stop\s(@\S+)$"))
async def stop_spam(client, message):
    chat = re.match(r"^stop\s(@\S+)$", message.text).group(1)
    if chat not in tasks:
        await message.reply("нет активной задачи для этого чата.")
        return
    tasks[chat].cancel()
    del tasks[chat]
    await message.reply(f"остановлено для {chat}")

app.run()
