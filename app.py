import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
import os

# Set your API key here or use environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your_openai_api_key")

# Initialize the OpenAI chat model
llm = ChatOpenAI(api_key=OPENAI_API_KEY, temperature=0.7)

# Memory to maintain conversation context
memory = ConversationBufferMemory()

# Conversation chain setup
chat_chain = ConversationChain(llm=llm, memory=memory)

# Function to generate a learning pathway
def generate_learning_pathway(user_level, interest):
    prompt = f"Create a learning pathway for a user who is at a {user_level} level and wants to learn about {interest}. Include books and steps."
    response = chat_chain.predict(input=prompt)
    return response

# Streamlit UI setup
st.set_page_config(page_title="The Library", layout="wide")

st.title("📚 The Library: AI Learning Assistant")
st.write("Your personal AI guide for discovering and learning about Artificial Intelligence.")

# Your Personal Librarian Section
st.header("Ask Your Personal Librarian")

# User input for AI learning interest
user_interest = st.text_input("What specific AI topic are you interested in?")

# Dropdown for AI knowledge level
user_level = st.selectbox("Select your AI knowledge level:", ["Beginner", "Intermediate", "Advanced"])

# Button to generate learning pathway
if st.button("Get Learning Pathway"):
    if user_interest and user_level:
        with st.spinner("Generating your personalized learning pathway..."):
            pathway = generate_learning_pathway(user_level, user_interest)
        st.subheader("🚀 Your Personalized Learning Pathway:")
        st.write(pathway)
    else:
        st.warning("Please enter an AI topic and select your knowledge level.")

st.sidebar.title("About The Library")
st.sidebar.info(
    "Created with Streamlit, LangChain, and GPT-4. Explore, learn, and master AI concepts with ease!"
)
