from database import files_col
import math

def format_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"

async def search_files_db(query, page, results_per_page):
    words = query.split()
    regex_queries = [
        {"$or": [
            {"file_name": {"$regex": w, "$options": "i"}},
            {"caption": {"$regex": w, "$options": "i"}}
        ]} for w in words
    ]
    
    db_query = {"$and": regex_queries}
    total_results = await files_col.count_documents(db_query)
    
    skip = (page - 1) * results_per_page
    cursor = files_col.find(db_query).skip(skip).limit(results_per_page)
    results = await cursor.to_list(length=results_per_page)
    
    return results, total_results
