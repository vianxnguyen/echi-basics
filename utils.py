from pymongo import MongoClient
def get_db_handle(db_name):
    client = MongoClient("mongodb://localhost:27017/")
    db_handle = client[db_name]
    return db_handle

def get_collection_handle(db_handle,collection_name):
    return db_handle[collection_name]

