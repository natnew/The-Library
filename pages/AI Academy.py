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

st.title("📚 The Library: AI Academy")


####

# Function to load and split PDF content into chunks
def load_course_material(course_name):
    course_path = Path(f"data/courses/{course_name}.pdf")
    if not course_path.exists():
        return ["Course material not found."]
    
    text_chunks = []
    with open(course_path, "rb") as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        for page in reader.pages:
            text_chunks.append(page.extract_text())
    
    # Splitting into smaller chunks for streaming
    chunk_size = 500  # Adjust chunk size as needed
    chunked_text = [text_chunks[i:i + chunk_size] for i in range(0, len(text_chunks), chunk_size)]
    return [" ".join(chunk) for chunk in chunked_text]


# Dropdown for course selection
courses = [
    "Intro to Prompt Engineering",
    "Advanced Prompt Engineering",
    "Intro to AI Agents",
    "Intro to RAG",
    "Advanced RAG",
    "Intro to Building AI Apps",
    "Responsible AI",
    "Building with Generative AI"
]

selected_course = st.selectbox("Select a course:", courses)

# Load and display course material
if selected_course:
    st.subheader(selected_course)

    # Load course material into session state if not already loaded
    if "course_material" not in st.session_state or st.session_state["current_course"] != selected_course:
        st.session_state["course_material"] = load_course_material(selected_course)
        st.session_state["current_chunk"] = 0
        st.session_state["current_course"] = selected_course

    # Display the current chunk of material
    course_material = st.session_state["course_material"]
    if st.session_state["current_chunk"] < len(course_material):
        st.text_area("Course Material", course_material[st.session_state["current_chunk"]], height=300)

        # Navigation buttons
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Previous", key="prev") and st.session_state["current_chunk"] > 0:
                st.session_state["current_chunk"] -= 1
        with col2:
            if st.button("Next", key="next") and st.session_state["current_chunk"] < len(course_material) - 1:
                st.session_state["current_chunk"] += 1
    else:
        st.write("You've reached the end of the course material.")