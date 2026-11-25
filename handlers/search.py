from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import config
import uuid
import datetime
from database import queries_col, add_user
from search import search_files_db, format_size
import math

@Client.on_message(filters.private & filters.text & ~filters.command(["start", "help", "stats", "index", "reindex", "broadcast"]))
async def handle_search(client: Client, message: Message):
    await add_user(message.from_user.id)
    query = message.text.strip()
    
    if len(query) < 2:
        return await message.reply("❌ Search query must be at least 2 characters long.")
        
    results, total_results = await search_files_db(query, page=1, results_per_page=config.RESULTS_PER_PAGE)
    
    if not results:
        return await message.reply("❌ No matching files found.\nPlease try another name or keyword.", quote=True)
        
    query_id = uuid.uuid4().hex[:8]
    await queries_col.insert_one({
        "_id": query_id, 
        "query": query, 
        "expireAt": datetime.datetime.utcnow()
    })
    
    buttons = []
    for file in results:
        name = file.get('file_name', f"File {file['message_id']}")
        size = format_size(file.get('file_size', 0))
        btn_text = f"[{size}] {name}"
        buttons.append([InlineKeyboardButton(btn_text, callback_data=f"get#{file['message_id']}")])
        
    total_pages = math.ceil(total_results / config.RESULTS_PER_PAGE)
    
    nav_buttons = []
    if total_pages > 1:
        nav_buttons.append(InlineKeyboardButton("Next ➡️", callback_data=f"next#{query_id}#2"))
        
    if nav_buttons:
        buttons.append(nav_buttons)
        
    await message.reply(
        f"🔎 **Search Results for:** `{query}`\n📄 Page 1 of {total_pages}\n🔢 Total files: {total_results}",
        reply_markup=InlineKeyboardMarkup(buttons),
        quote=True
    )

@Client.on_message(filters.chat(config.CHANNEL_ID) & (filters.document | filters.video | filters.audio | filters.photo))
async def auto_indexer(client: Client, message: Message):
    from database import save_file
    await save_file(message)
