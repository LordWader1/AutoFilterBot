from motor.motor_asyncio import AsyncIOMotorClient
import config

client = AsyncIOMotorClient(config.DATABASE_URL)
db = client['autofilter_bot']

files_col = db['files']
users_col = db['users']
queries_col = db['queries']

async def init_db():
    await files_col.create_index([('file_name', 1)])
    await files_col.create_index([('caption', 'text')])
    await files_col.create_index([('message_id', 1)], unique=True)
    await queries_col.create_index("expireAt", expireAfterSeconds=86400)

async def add_user(user_id):
    await users_col.update_one({'user_id': user_id}, {'$set': {'user_id': user_id}}, upsert=True)

async def total_users():
    return await users_col.count_documents({})

async def total_files():
    return await files_col.count_documents({})

async def save_file(message):
    media = message.document or message.video or message.audio or message.animation or message.photo
    if not media:
        return False

    if message.photo:
        media = message.photo[-1]
        file_name = f"Photo_{message.id}.jpg"
        file_type = "photo"
    else:
        file_name = getattr(media, 'file_name', f"File_{message.id}")
        file_type = media.__class__.__name__.lower()

    file_size = getattr(media, 'file_size', 0)
    caption = message.caption or ""
    
    doc = {
        'message_id': message.id,
        'channel_id': message.chat.id,
        'file_name': file_name,
        'caption': caption,
        'file_id': media.file_id,
        'file_type': file_type,
        'file_size': file_size,
    }
    
    await files_col.update_one({'message_id': message.id}, {'$set': doc}, upsert=True)
    return True

async def delete_file(message_id):
    await files_col.delete_one({'message_id': message_id})
