from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

uri = os.getenv("MDB_URI", "")
db_name = os.getenv("MDB_DBNAME", "")

client = AsyncIOMotorClient(uri)
db = client[db_name]

async def connect_to_mongo():
    try:
        await db.command("ping")
        print("Connected to MongoDB!")
    except Exception as e:
        print("MongoDB connection error:", e)

async def close_mongo_connection():
    client.close()
    print("MongoDB connection closed.")
