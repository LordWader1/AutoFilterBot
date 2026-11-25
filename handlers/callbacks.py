from pyrogram import Client
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
import config
from database import queries_col, files_col, delete_file
from search import search_files_db, format_size
import math

@Client.on_callback_query()
async def callback_handlers(client: Client, query: CallbackQuery):
    data = query.data
    
    if data.startswith("get#"):
        message_id = int(data.split("#")[1])
        await query.answer("⏳ Please wait! Your requested file is being prepared.", show_alert=False)
        
        try:
            await client.copy_message(
                chat_id=query.from_user.id,
                from_chat_id=config.CHANNEL_ID,
                message_id=message_id
            )
            await client.send_message(query.from_user.id, "✅ Your file has been sent successfully!")
        except Exception as e:
            error_msg = str(e)
            if "MESSAGE_ID_INVALID" in error_msg or "MESSAGE_DELETED" in error_msg:
                await delete_file(message_id)
                await query.message.reply("❌ This file has been removed from the database.")
            else:
                await query.message.reply("❌ Failed to send file. Contact admin.")
            
    elif data.startswith("next#") or data.startswith("prev#"):
        action, query_id, page_str = data.split("#")
        page = int(page_str)
        
        query_doc = await queries_col.find_one({"_id": query_id})
        if not query_doc:
            return await query.answer("❌ Search session expired. Please search again.", show_alert=True)
            
        search_str = query_doc['query']
        results, total_results = await search_files_db(search_str, page, config.RESULTS_PER_PAGE)
        
        buttons = []
        for file in results:
            name = file.get('file_name', f"File {file['message_id']}")
            size = format_size(file.get('file_size', 0))
            buttons.append([InlineKeyboardButton(f"[{size}] {name}", callback_data=f"get#{file['message_id']}")])
            
        total_pages = math.ceil(total_results / config.RESULTS_PER_PAGE)
        
        nav_buttons = []
        if page > 1:
            nav_buttons.append(InlineKeyboardButton("⬅️ Prev", callback_data=f"prev#{query_id}#{page-1}"))
        if page < total_pages:
            nav_buttons.append(InlineKeyboardButton("Next ➡️", callback_data=f"next#{query_id}#{page+1}"))
            
        if nav_buttons:
            buttons.append(nav_buttons)
            
        await query.message.edit_text(
            f"🔎 **Search Results for:** `{search_str}`\n📄 Page {page} of {total_pages}\n🔢 Total files: {total_results}",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
