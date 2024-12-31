import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
import os
import time




st.set_page_config(
    page_title="Chatbot",
    page_icon="🤖",  # You can use an emoji or a path to an image file
    layout="wide"    # Options are "centered" or "wide"
)


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

# Generator function to stream the learning pathway
def stream_learning_pathway(user_level, interest):
    pathway = generate_learning_pathway(user_level, interest)
    for word in pathway.split():
        yield word + " "
        time.sleep(0.05)  # Adjust the sleep time for desired streaming speed

# Streamlit UI setup
#st.set_page_config(page_title="The Library", layout="wide")

st.title("📚 The Library: AI Learning Assistant")
st.write("Your personal AI guide for discovering and learning about Artificial Intelligence.")

# Your Personal Librarian Section
st.header("Your Personal Librarian")

# User input for AI learning interest
user_interest = st.text_input("What specific AI topic are you interested in?")

# Dropdown for AI knowledge level
user_level = st.selectbox("Select your AI knowledge level:", ["Beginner", "Intermediate", "Advanced"])

# Button to generate learning pathway
if st.button("Get Learning Pathway"):
    if user_interest and user_level:
        with st.spinner("Generating your personalized learning pathway..."):
            st.write_stream(stream_learning_pathway(user_level, user_interest))
    else:
        st.warning("Please enter an AI topic and select your knowledge level.")


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
