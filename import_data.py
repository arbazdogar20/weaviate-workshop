import json
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
from weaviate import connect_to_wcs
from weaviate.auth import AuthApiKey
import config

# Load JSON
with open("sample_mflix.movies.json", "r") as f:
    movies_data = json.load(f)

# Connect to Weaviate
client = connect_to_wcs(
    cluster_url=config.WEAVIATE_URL,
    auth_credentials=AuthApiKey(config.WEAVIATE_API_KEY),
    skip_init_checks=True
)

# Use smaller schema if in workshop mode
schema = {
    "class": "Movie",
    "vectorizer": "none",
    "properties": [
        {"name": "title", "dataType": ["text"]},
        {"name": "plot", "dataType": ["text"]},
        {"name": "genres", "dataType": ["text[]"]},
        {"name": "year", "dataType": ["number"]}
    ]
}

# Recreate schema (dev only!)
if "Movie" in client.collections.list_all():
    client.collections.delete("Movie")
client.collections.create_from_dict(schema)

# Init embed model
model = SentenceTransformer("all-MiniLM-L6-v2")
collection = client.collections.get("Movie")

# Import
for movie in tqdm(movies_data[:1000], desc="Importing"):
    try:
        text = f"{movie['title']}: {movie.get('plot', '')}"
        embedding = model.encode(text).tolist()
        collection.data.insert(
            properties={
                "title": movie["title"],
                "plot": movie.get("plot", ""),
                "genres": movie.get("genres", []),
                "year": movie.get("year", 0)
            },
            vector=embedding
        )
    except Exception as e:
        print(f"Error: {movie.get('title')} – {e}")

print("✅ Data import complete!")
client.close()
