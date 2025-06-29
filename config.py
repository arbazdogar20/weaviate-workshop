# config.py
import os

MONGO_URI = os.getenv("MONGO_URI")
WEAVIATE_URL = os.getenv("WEAVIATE_URL")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")