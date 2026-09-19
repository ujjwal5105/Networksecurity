from pymongo import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os
import certifi

load_dotenv()

# FIX: Using unique keys to avoid Windows OS variable conflicts
username = os.getenv("MONGO_USER")
raw_password = os.getenv("MONGO_PASS") or ""
password = quote_plus(raw_password)

# Print debug info to your terminal so you can see exactly what Python reads
print(f"DEBUG: Attempting login with Username: '{username}'")

uri = f"mongodb+srv://{username}:{password}@ac-jisg9r6.flqalgx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

print("🔄 Attempting deployment handshake...")

client = MongoClient(
    uri,
    server_api=ServerApi("1"),
    tls=True,
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=10000
)

try:
    client.admin.command("ping")
    print("\n🎉 Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print("\n❌ MongoDB connection FAILED")
    print(f"Error Type: {type(e).__name__}")
    print(f"Details: {e}")
# Add this at the end of test_mongo.py
databases = client.list_database_names()
print("\n📂 Actual Databases in your Atlas Cluster:", databases)

for db_name in databases:
    if db_name not in ['admin', 'local']:
        print(f"   ↳ Collections inside '{db_name}':", client[db_name].list_collection_names())
