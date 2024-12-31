import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
import os
import time


# Streamlit sidebar for user selection
st.sidebar.title(":streamlit: The Library")
st.sidebar.write("This tool is designed to help you explore and learn about AI.")
# Add this note to the sidebar:
st.sidebar.write("Accuracy, correctness, or appropriateness cannot be guaranteed.")

st.sidebar.write(
       "Built by [Natasha Newbold](https://www.linkedin.com/in/natasha-newbold/) "
            )

# Check if API key is provided
if os.getenv("OPENAI_API_KEY"):
    st.sidebar.success("✅ API key already provided!")
else:
    st.sidebar.error("❌ API key not provided. Please set your OpenAI API key.")
st.sidebar.info(
    "Created with Streamlit, LangChain, and GPT-4. Explore, learn, and master AI concepts with ease!"
)



####
podcasts = [
    {
        "title": "Attention Is All You Need",
        "duration": "4 min",
        "image_url": "https://path/to/attention-is-all-you-need.jpg",
        "audio_url": "https://path/to/attention-is-all-you-need-audio.mp3",
        "source_link": "https://example.com/research-paper-1"
    },
    {
        "title": "Artificial Intelligence Index Report 2024",
        "duration": "8 min",
        "image_url": "https://path/to/ai-index-report.jpg",
        "audio_url": "https://path/to/ai-index-report-audio.mp3",
        "source_link": "https://example.com/research-paper-2"
    },
    # ... add as many as you like ...
]

#####
def display_podcast_tile(podcast):
    """
    Helper function to display one 'tile' for a single podcast.
    """
    st.image(podcast["image_url"], use_column_width=True)
    st.write(f"### {podcast['title']}")
    st.write(f"**Duration:** {podcast['duration']}")
    if podcast["audio_url"]:
        # If you have a direct .mp3 URL, st.audio can embed an audio player
        st.audio(podcast["audio_url"], format="audio/mp3")
    if podcast["source_link"]:
        st.markdown(f"[View Source]({podcast['source_link']})")
    # Provide a 'Play' button if you want a separate action – you can handle it as needed
    # if st.button(f"Play {podcast['title']}"):
    #     # Do something on click, e.g. st.audio(podcast["audio_url"])

# Main section
def display_podcast_tile(podcast):
    # Show image (replacing use_column_width)
    st.image(podcast["image_url"], use_container_width=True)
    st.markdown(f"### {podcast['title']}")
    st.write(f"**Duration:** {podcast['duration']}")
    if podcast["audio_url"]:
        st.audio(podcast["audio_url"], format="audio/mp3")
    if podcast["source_link"]:
        st.markdown(f"[View Source]({podcast['source_link']})")


num_cols = 3  # how many tiles per row
for i in range(0, len(podcasts), num_cols):
    cols = st.columns(num_cols)
    for col_index in range(num_cols):
        if i + col_index < len(podcasts):
            with cols[col_index]:
                display_podcast_tile(podcasts[i + col_index])
