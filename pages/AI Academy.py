import streamlit as st
import os
import time
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
import json


# App Configuration
st.set_page_config(page_title="The Library: AI Academy", layout="wide")

# Page Title
st.title("📚 The Library: AI Academy")
st.write("Courses on Artificial Intelligence.")

# Load API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", None)
if not OPENAI_API_KEY:
    st.error("API key not found. Please configure the API key in Streamlit secrets.")
    st.stop()

# Initialize the OpenAI chat model
llm = ChatOpenAI(api_key=OPENAI_API_KEY, temperature=0.7)

# Memory to maintain conversation context
memory = ConversationBufferMemory()

# Conversation chain setup
chat_chain = ConversationChain(llm=llm, memory=memory)

# Streamlit sidebar for user selection
st.sidebar.title(":streamlit: The Library")
st.sidebar.write("This tool is designed to help you explore and learn about AI.")
# Add this note to the sidebar:
st.sidebar.write("Accuracy, correctness, or appropriateness cannot be guaranteed.")

st.sidebar.write(
       "Built by [Natasha Newbold](https://www.linkedin.com/in/natasha-newbold/) "
)

st.sidebar.info(
    "Created with Streamlit, LangChain, and GPT-4. Explore, learn, and master AI concepts with ease!"
)

# Course Modules
courses = {
    "Intro to Prompt Engineering": [
        "Understanding Prompt Basics",
        "Crafting Effective Prompts",
        "Prompt Formats and Structures",
        "Role of Context in Prompting",
        "Iterative Prompting",
        "Evaluating Prompt Effectiveness",
        "Prompting for Creativity",
        "Handling Ambiguity in Prompts",
        "Bias and Ethical Prompting",
        "Prompt Experimentation Lab"
    ],
    "Advanced Prompt Engineering": [
        "Advanced Prompt Structures",
        "Dynamic Prompt Design",
        "Using Few-Shot Learning",
        "Fine-Tuning with Prompts",
        "Chaining Prompts Effectively",
        "Leveraging GPT Tools",
        "Debugging Prompt Failures",
        "Optimising Prompts for Outputs",
        "Prompt Analysis Frameworks",
        "Advanced Prompt Experimentation Lab"
    ],
    "Intro to AI Agents": [
        "What Are AI Agents?",
        "Building Blocks of AI Agents",
        "Use Cases for AI Agents",
        "Simple AI Agent Design",
        "Multi-Agent Collaboration",
        "Challenges in AI Agents",
        "Integrating Agents with Tools",
        "Agent Planning and Reasoning",
        "Feedback Loops in Agents",
        "AI Agent Development Lab"
    ],
    "Intro to RAG": [
        "What is RAG (Retrieval-Augmented Generation)?",
        "Core Components of RAG",
        "Knowledge Bases and Indexing",
        "Designing Effective Retrieval Mechanisms",
        "Integrating GPT with RAG",
        "RAG Pipelines in Action",
        "Handling RAG Failures",
        "Performance Optimisation in RAG",
        "Case Studies in RAG",
        "Building RAG Systems Lab"
    ],
    "Advanced RAG": [
        "Scalable RAG Architectures",
        "Fine-Tuning Knowledge Bases",
        "Hybrid Retrieval Techniques",
        "Optimising RAG Pipelines",
        "Using RAG for Complex Queries",
        "Multi-Modal RAG Systems",
        "RAG and Continual Learning",
        "Monitoring RAG Systems",
        "RAG in Industry Applications",
        "Advanced RAG Systems Lab"
    ],
    "Intro to Building AI Apps": [
        "Overview of AI Applications",
        "Designing User-Centric AI Apps",
        "Selecting Models for Applications",
        "Integrating APIs with Apps",
        "Real-Time AI Systems",
        "Frontend and Backend Coordination",
        "AI App Deployment",
        "Maintaining AI Applications",
        "Scaling AI Applications",
        "Building AI Apps Lab"
    ],
    "Responsible AI": [
        "Principles of Responsible AI",
        "Ethical AI Design",
        "Bias Detection and Mitigation",
        "Transparency and Explainability",
        "Data Privacy in AI",
        "Regulatory Compliance",
        "Monitoring and Accountability",
        "Human-AI Collaboration",
        "Case Studies in Responsible AI",
        "Building Responsible AI Lab"
    ],
    "Building with Generative AI": [
        "Introduction to Generative AI",
        "Generative AI Use Cases",
        "Training Generative Models",
        "Designing for Creativity",
        "Integrating Generative AI Tools",
        "Ethics in Generative AI",
        "Optimising Generative Systems",
        "Multi-Modal Generative AI",
        "Scaling Generative AI Systems",
        "Generative AI Development Lab"
    ]
}

# Sidebar for Course and Module Selection
selected_course = st.sidebar.selectbox("Select a Course", list(courses.keys()), key="course_select")
selected_module = st.sidebar.selectbox("Select a Module", courses[selected_course], key="module_select")

st.header(f"{selected_course} - {selected_module}")
st.write("Ask a question related to the selected module below:")

# Function to stream the response as sentences
def stream_response_sentences(response_text):
    sentences = response_text.split('. ')
    for sentence in sentences:
        yield sentence.strip() + '. '
        time.sleep(0.5)

# Input for User Questions
user_input = st.text_input("Your Question", key="user_question")
if user_input:
    try:
        context = f"You are an AI expert teaching the course '{selected_course}' and the module '{selected_module}'. You answer in full sentences using a minimum of 150 words. You answer in simple language and provide information on the topics."
        response = chat_chain.run(input=f"{context} {user_input}")
        streamed_response = stream_response_sentences(response)
        st.write_stream(streamed_response)
    except Exception as e:
        st.error(f"An error occurred: {e}")


# Add "Build Projects" Section Below the Existing UI
# Load JSON Data
def load_projects():
    try:
        with open("data/projects.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("Project data not found. Please add a 'projects.json' file in the 'data' folder.")
        return {}

# Load Project Data
project_data = load_projects()

# Build Projects Section
st.subheader("Build Projects")
st.write("Here are some hands-on projects related to this module. Click on 'Build this' to access the corresponding GitHub repository.")

# Check if there are projects for the selected course
if selected_course in project_data:
    module_projects = project_data[selected_course]
    
    # Display Project Cards
    cols = st.columns(3)  # Three projects per row
    for i, project in enumerate(module_projects):
        with cols[i % 3]:  # Cycle through columns
            st.image(project["image_url"], use_container_width=True)  # Display the project image
            st.markdown(f"### {project['title']}")
            st.write(project["description"])
            st.markdown(f"[Build this]( {project['github_url']} )", unsafe_allow_html=True)
else:
    st.info("No projects available for this module.")
