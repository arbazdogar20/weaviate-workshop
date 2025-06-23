from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
import config

# ✅ UPDATE with your MongoDB URI & DB name
MONGO_URI = config.MONGO_URI
DB_NAME = "search-enginee"    # your database name
COLLECTION_NAME = "movies"     # your collection name

# Connect
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Embed each movie's plot/fullplot
for doc in collection.find():
    text = doc.get("fullplot") or doc.get("plot") or doc.get("description") or doc.get("title")
    if text:
        embedding = model.encode(text).tolist()
        collection.update_one(
            {"_id": doc["_id"]},
            {"$set": {"embedding": embedding}}
        )

print("✅ Embeddings added to all movies!")

client.close()
