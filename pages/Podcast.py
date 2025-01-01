import streamlit as st
import json
import os

# Load podcasts from the JSON file located in the 'data' folder
json_file_path = os.path.join("data", "podcasts.json")
with open(json_file_path, "r") as file:
    podcasts = json.load(file)

# Streamlit sidebar
st.sidebar.title(":streamlit: The Library")
st.sidebar.write("This tool is designed to help you explore and learn about AI.")
st.sidebar.write("Accuracy, correctness, or appropriateness cannot be guaranteed.")
st.sidebar.write(
    "Built by [Natasha Newbold](https://www.linkedin.com/in/natasha-newbold/)"
)
if os.getenv("OPENAI_API_KEY"):
    st.sidebar.success("✅ API key already provided!")
else:
    st.sidebar.error("❌ API key not provided. Please set your OpenAI API key.")
st.sidebar.info(
    "Created with Streamlit, LangChain, and GPT-4. Explore, learn, and master AI concepts with ease!"
)

st.title("📚 The Library: Podcast")


BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Directory of the script
IMAGE_DIR = os.path.join(BASE_DIR, "data", "images")

def display_podcast_tile(podcast):
    image_path = os.path.join(IMAGE_DIR, podcast["image_url"])
    if os.path.exists(image_path):
        st.image(image_path, use_container_width=True)
    else:
        st.error(f"Image not found: {image_path}")
    st.markdown(f"### {podcast['title']}")
    st.write(f"**Duration:** {podcast['duration']}")
    if podcast["audio_url"]:
        st.audio(podcast["audio_url"], format="audio/mp3")
    if podcast["source_link"]:
        st.markdown(f"[View Source]({podcast['source_link']})")