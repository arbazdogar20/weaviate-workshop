import streamlit as st
from sentence_transformers import SentenceTransformer
from weaviate.auth import AuthApiKey
from weaviate import connect_to_wcs
import config

WEAVIATE_URL = config.WEAVIATE_URL
WEAVIATE_API_KEY = config.WEAVIATE_API_KEY
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# --- Connect to Weaviate ---
@st.cache_resource
def connect_weaviate():
    return connect_to_wcs(
        cluster_url=WEAVIATE_URL,
        auth_credentials=AuthApiKey(WEAVIATE_API_KEY),
        skip_init_checks=True
    )

# --- Load model once ---
@st.cache_resource
def load_model():
    return SentenceTransformer(EMBEDDING_MODEL)

# --- UI Layout ---
st.set_page_config("Movie Mind Reader", layout="wide")
st.title("🧠🎬 Movie Mind Reader")
st.caption("Discover movies by meaning, not just keywords!")

query = st.text_input("What kind of movie are you looking for?", placeholder="e.g. mystery with a twist ending")
top_k = st.slider("Number of results", 1, 15, 5)

# --- Main logic ---
if query:
    with st.spinner("Thinking..."):
        try:
            client = connect_weaviate()
            model = load_model()
            collection = client.collections.get("Movie")

            vector = model.encode(query).tolist()

            results = collection.query.near_vector(
                near_vector=vector,
                limit=top_k,
                return_properties=["title", "plot", "genres", "year"],
                return_metadata=["distance"]
            )

            if not results.objects:
                st.warning("No results found. Try a broader query.")
            else:
                for obj in results.objects:
                    props = obj.properties
                    st.markdown(f"### 🎥 {props.get('title', 'Untitled')} ({props.get('year', 'N/A')})")
                    st.write(f"**Genres:** {', '.join(props.get('genres', []))}")
                    st.write(f"**Plot:** {props.get('plot', 'No plot available')}")
                    st.write(f"**Similarity Score:** `{obj.metadata.distance:.4f}`")
                    st.markdown("---")

        except Exception as e:
            st.error(f"Something went wrong: {e}")
