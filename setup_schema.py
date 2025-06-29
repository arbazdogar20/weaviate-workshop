import os
from dotenv import load_dotenv
from weaviate.auth import AuthApiKey
from weaviate import connect_to_wcs

# Load .env values
load_dotenv()
WEAVIATE_URL = os.getenv("WEAVIATE_URL")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")

client = connect_to_wcs(
    cluster_url=WEAVIATE_URL,
    auth_credentials=AuthApiKey(WEAVIATE_API_KEY),
    skip_init_checks=True
)

# Define schema (keep it small if testing)
movie_schema = {
    "class": "Movie",
    "description": "A movie from the sample dataset",
    "vectorizer": "none",
    "properties": [
        {"name": "title", "dataType": ["text"]},
        {"name": "plot", "dataType": ["text"]},
        {"name": "genres", "dataType": ["text[]"]},
        {"name": "year", "dataType": ["number"]}
    ]
}

# Create only if it doesn't exist
existing_classes = [col.name for col in client.collections.list_all()]
if "Movie" not in existing_classes:
    client.collections.create_from_dict(movie_schema)
    print("✅ 'Movie' class created in Weaviate schema.")
else:
    print("ℹ️ 'Movie' class already exists.")

client.close()
