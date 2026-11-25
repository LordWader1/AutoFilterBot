from pyrogram import Client, filters
from pyrogram.types import Message
import config
from indexer import index_channel_history
from database import total_users, total_files, files_col
import asyncio

async def is_admin(_, __, message):
    return message.from_user and message.from_user.id == config.ADMIN_ID

admin_filter = filters.create(is_admin)

@Client.on_message(filters.private & filters.command("stats") & admin_filter)
async def stats_cmd(client: Client, message: Message):
    users = await total_users()
    files = await total_files()
    await message.reply(f"📊 **Bot Statistics:**\n\n👥 Total Users: `{users}`\n📂 Total Indexed Files: `{files}`")

@Client.on_message(filters.private & filters.command("index") & admin_filter)
async def index_cmd(client: Client, message: Message):
    status_msg = await message.reply("⏳ Starting indexing task...")
    asyncio.create_task(index_channel_history(client, status_msg))

@Client.on_message(filters.private & filters.command("reindex") & admin_filter)
async def reindex_cmd(client: Client, message: Message):
    await files_col.drop()
    status_msg = await message.reply("🗑 Database cleared. ⏳ Starting fresh indexing...")
    asyncio.create_task(index_channel_history(client, status_msg))

@Client.on_message(filters.private & filters.command("broadcast") & admin_filter)
async def broadcast_cmd(client: Client, message: Message):
    if not message.reply_to_message:
        return await message.reply("Reply to a message to broadcast it.")
    
    await message.reply("Broadcasting started...")
    from database import users_col
    success, failed = 0, 0
    
    async for user in users_col.find():
        try:
            await message.reply_to_message.copy(user['user_id'])
            success += 1
            await asyncio.sleep(0.1)
        except:
            failed += 1
            
    await message.reply(f"✅ Broadcast Complete.\nSuccess: {success}\nFailed: {failed}")
