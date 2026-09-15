from pymongo import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os
load_dotenv()



username = "hanji0877_db_user"
password = quote_plus("Ujjwal@123")

uri = f"mongodb+srv://{username}:{password}@cluster0.flqalgx.mongodb.net/?appName=Cluster0"

client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)