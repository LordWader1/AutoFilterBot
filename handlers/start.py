from pyrogram import Client, filters
from pyrogram.types import Message
from database import add_user
import config

@Client.on_message(filters.private & filters.command("start"))
async def start_cmd(client: Client, message: Message):
    await add_user(message.from_user.id)
    
    welcome_text = (
        f"👋 Welcome to **{config.BOT_NAME}**!\n\n"
        "🔎 Search for any movie, series, document, or file by sending its name or keyword.\n"
        "📂 I'll search my database and show you matching files.\n\n"
        "👇 Simply type what you're looking for!"
    )
    await message.reply(welcome_text, quote=True)

@Client.on_message(filters.private & filters.command("help"))
async def help_cmd(client: Client, message: Message):
    help_text = (
        "**How to use this bot:**\n"
        "1. Just type the name of the movie/file you want.\n"
        "2. Click on the button from the search results.\n"
        "3. The bot will send the file directly to you.\n\n"
        "Note: Minor spelling mistakes might lead to no results, try to be accurate!"
    )
    await message.reply(help_text, quote=True)
