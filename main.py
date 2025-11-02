from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import InputStream, AudioPiped
import asyncio, os

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
SESSION_STRING = os.getenv("SESSION_STRING")

bot = Client("KazamaMusicBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user = Client("UserBot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
vc = PyTgCalls(user)

@bot.on_message(filters.command("start"))
async def start(_, message):
    await message.reply_text("🎵 Welcome to **Kazama Music Bot**!\nUse `/play` to play songs in VC.")

@bot.on_message(filters.command("play"))
async def play(_, message):
    chat_id = message.chat.id
    if len(message.command) < 2:
        return await message.reply_text("Please provide a song URL or name!")
    url = message.text.split(" ", 1)[1]
    await message.reply_text("🔊 Joining VC and playing music...")
    await vc.join_group_call(chat_id, InputStream(AudioPiped(url)))
    await message.reply_text("🎶 Now playing!")

@bot.on_message(filters.command("stop"))
async def stop(_, message):
    chat_id = message.chat.id
    await vc.leave_group_call(chat_id)
    await message.reply_text("⏹️ Stopped the music and left VC.")

async def main():
    await user.start()
    await vc.start()
    await bot.start()
    print("✅ Kazama Music Bot is running...")
    await idle()
    await bot.stop()
    await vc.stop()
    await user.stop()

if __name__ == "__main__":
    from pyrogram import idle
    asyncio.run(main())
