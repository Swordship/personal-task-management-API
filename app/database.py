import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from beanie import init_beanie

load_dotenv()
class Database:
    client : AsyncIOMotorClient = None
async def connect_to_monogoDB():
    Database.client = AsyncIOMotorClient(os.getenv("MONGODB_URL"))
    print("Mongodb Connected")

async def disconnect_to_monogoDB():
    Database.client.close()
    print("mongodb disconnected")

async def __init__database():
    
    
    pass