from pymongo import MongoClient
from config import MONGO_URI, MONGO_DB_NAME

try:
    client = MongoClient(MONGO_URI)
    database = client[MONGO_DB_NAME]
except Exception as e:
    print(f"Error connecting to database: {e}")
