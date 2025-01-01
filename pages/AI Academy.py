import streamlit as st
import os
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

# App Configuration
st.set_page_config(page_title="AI Learning Hub", layout="wide")

# Load API Key
OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", None)
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

# Dropdown for Course Selection
selected_course = st.selectbox("Select a Course", list(courses.keys()))
selected_module = st.selectbox("Select a Module", courses[selected_course])

st.title(f"{selected_course} - {selected_module}")
st.write("Ask a question related to the selected module below:")

# Input for User Questions
user_input = st.text_input("Your Question")
if user_input:
    with st.spinner("Generating response..."):
        try:
            context = f"You are an expert teaching the course '{selected_course}' and the module '{selected_module}'."
            answer = chat_chain.run(input=f"{context} {user_input}")
            st.markdown(f"### Answer:\n{answer}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
