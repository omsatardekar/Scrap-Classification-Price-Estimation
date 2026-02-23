from pymongo import MongoClient
from app.core.config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client["scrapx"]

users_collection = db["users"]
orders_collection = db["orders"]
