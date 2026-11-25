import config
from database import save_file

async def index_channel_history(client, status_message):
    count = 0
    await status_message.edit("⏳ **Indexing started... Please wait.**")
    try:
        async for message in client.get_chat_history(config.CHANNEL_ID):
            saved = await save_file(message)
            if saved:
                count += 1
                
            if count % 200 == 0:
                await status_message.edit(f"⏳ **Indexing in progress...**\nIndexed {count} files so far.")
                
        await status_message.edit(f"✅ **Indexing Complete!**\nSuccessfully indexed **{count}** files.")
    except Exception as e:
        await status_message.edit(f"❌ **Error during indexing:**\n`{str(e)}`")
        
