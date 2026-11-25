from pyrogram import Client, idle
import config
from database import init_db
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

async def main():
    await init_db()
    
    app = Client(
        "AutoFilterBot",
        api_id=config.API_ID,
        api_hash=config.API_HASH,
        bot_token=config.BOT_TOKEN,
        plugins=dict(root="handlers")
    )
    
    await app.start()
    logging.info(f"Bot Started as @{(await app.get_me()).username}")
    
    if config.SESSION_STRING:
        user_app = Client(
            "UserBot",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=config.SESSION_STRING
        )
        await user_app.start()
        logging.info("User Session Started")
        
    await idle()
    
    await app.stop()
    if config.SESSION_STRING:
        await user_app.stop()

if __name__ == "__main__":
    asyncio.run(main())
