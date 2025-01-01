import streamlit as st
import json
import os

# Load podcasts from the JSON file located in the 'data' folder
json_file_path = os.path.join("data", "podcasts.json")
try:
    with open(json_file_path, "r") as file:
        podcasts = json.load(file)
except FileNotFoundError:
    st.error(f"Could not find the JSON file at {json_file_path}. Please check the path.")
    podcasts = []

# Streamlit sidebar
st.sidebar.title(":streamlit: The Library")
st.sidebar.write("This tool is designed to help you explore and learn about AI.")
st.sidebar.write("Accuracy, correctness, or appropriateness cannot be guaranteed.")
st.sidebar.write("Built by [Natasha Newbold](https://www.linkedin.com/in/natasha-newbold/)")
if os.getenv("OPENAI_API_KEY"):
    st.sidebar.success("✅ API key already provided!")
else:
    st.sidebar.warning("API key not provided. Podcast tiles will still display.")
st.sidebar.info(
    "Created with Streamlit, LangChain, and GPT-4. Explore, learn, and master AI concepts with ease!"
)

st.title("📚 The Library: Podcast")

# Base directory for locating images
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "data", "images")

# Function to display a single podcast tile
def display_podcast_tile(podcast):
    image_path = os.path.join(IMAGE_DIR, podcast.get("image_url", ""))
    st.write(f"Debug: Image path is {image_path}")  # Debugging output
    if os.path.exists(image_path):
        st.image(image_path, use_container_width=True)
    else:
        st.error(f"Image not found: {image_path}")
    st.markdown(f"### {podcast['title']}")
    st.write(f"**Duration:** {podcast['duration']}")
    if podcast.get("audio_url"):
        st.audio(podcast["audio_url"], format="audio/mp3")
    if podcast.get("source_link"):
        st.markdown(f"[View Source]({podcast['source_link']})")

# Display podcasts in a grid layout
if podcasts:
    num_cols = 3  # Number of columns for the layout
    for i in range(0, len(podcasts), num_cols):
        cols = st.columns(num_cols)
        for col_index in range(num_cols):
            if i + col_index < len(podcasts):
                with cols[col_index]:
                    display_podcast_tile(podcasts[i + col_index])
else:
    st.error("No podcasts found in the JSON file.")
