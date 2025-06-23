import streamlit as st
from pymongo import MongoClient
import config

# MongoDB connection
client = MongoClient(config.MONGO_URI)
db = client["search-enginee"]
collection = db["movies"]

# Streamlit app setup
st.set_page_config(page_title="🎬 Movie Finder", page_icon="🎥", layout="wide")
st.title("🎬 Movie Finder")
st.write("Search for any movie by its name and view full details with poster, ratings, and more.")

# Search bar
query = st.text_input("🔍 Enter movie title")

if query:
    # Build flexible query: match "Title" or "title"
    results = list(collection.find({
        "$or": [
            {"Title": {"$regex": query, "$options": "i"}},
            {"title": {"$regex": query, "$options": "i"}}
        ]
    }))

    if not results:
        st.warning("❌ No movie found with that name.")
    else:
        for movie in results:
            st.markdown("----")
            cols = st.columns([1, 2])

            # Fallbacks: handle missing keys safely
            poster = movie.get("Poster") or movie.get("poster") or ""
            title = movie.get("Title") or movie.get("title") or "N/A"
            year = movie.get("Year") or movie.get("year") or "N/A"
            genre = movie.get("Genre") or movie.get("genre") or "N/A"
            director = movie.get("Director") or movie.get("director") or "N/A"
            runtime = movie.get("Runtime") or movie.get("runtime") or "N/A"
            imdb_rating = movie.get("imdbRating") or movie.get("imdb_rating") or "N/A"
            votes = movie.get("imdbVotes") or movie.get("imdb_votes") or "N/A"
            awards = movie.get("Awards") or movie.get("awards") or "N/A"
            box_office = movie.get("BoxOffice") or movie.get("box_office") or "N/A"
            plot = movie.get("Plot") or movie.get("plot") or "N/A"

            with cols[0]:
                if poster:
                    st.image(poster, width=200)
                else:
                    st.info("No poster available.")
            with cols[1]:
                st.markdown(f"### 🎞️ {title} ({year})")
                st.markdown(f"**🎭 Genre:** {genre}")
                st.markdown(f"**🎬 Director:** {director}")
                st.markdown(f"**🕒 Runtime:** {runtime}")
                st.markdown(f"**⭐ IMDb Rating:** {imdb_rating}")
                st.markdown(f"**🗳️ Votes:** {votes}")
                st.markdown(f"**🏆 Awards:** {awards}")
                st.markdown(f"**📦 Box Office:** {box_office}")
                st.markdown(f"**📖 Plot:** {plot}")
