from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
import weaviate
import config

# 1️⃣ MongoDB
mongo_client = MongoClient(config.MONGO_URI)
db = mongo_client[config.MONGO_DB]
collection = db[config.MONGO_COLLECTION]

# 2️⃣ Weaviate v3 style (matches your installed lib)
client = weaviate.Client(
    url=config.WEAVIATE_URL,  # FULL https:// URL
    auth_client_secret=weaviate.AuthApiKey(config.WEAVIATE_API_KEY)
)

# 3️⃣ Create schema if needed
class_name = "Document"

if not client.schema.contains({"classes": [{"class": class_name}]}):
    schema = {
        "classes": [
            {
                "class": class_name,
                "vectorizer": "none",
                "properties": [
                    {"name": "text", "dataType": ["text"]}
                ],
            }
        ]
    }
    client.schema.create(schema)

# 4️⃣ Embed & insert
model = SentenceTransformer('all-MiniLM-L6-v2')

for doc in collection.find():
    text = doc.get("text_field")  # Replace with your field!
    if not text:
        continue

    embedding = model.encode(text).tolist()

    client.data_object.create(
        data_object={"text": text},
        class_name=class_name,
        vector=embedding
    )

mongo_client.close()
print("✅ Import done using v3 syntax.")
