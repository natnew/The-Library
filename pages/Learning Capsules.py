
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
import os
import time
import random
from data.flashcards import flashcards


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

########
########

# --------------------------------------------------------------------
# 1. CSS for Bubble Layout
# --------------------------------------------------------------------
BUBBLE_CSS = """
<style>
.question-box {
    background-color: #1f1f1f;
    color: #ffffff;
    padding: 1.5rem;
    border-radius: 12px;
    margin: 1rem 0;
    border: 2px solid #dc3535; /* Red border for the speech bubble */
    position: relative;
}

.question-box::before {
    content: "";
    position: absolute;
    left: 20px;
    bottom: -20px;
    width: 0;
    height: 0;
    border: 20px solid transparent;
    border-top: 20px solid #dc3535; /* Tail under the bubble */
}

.question-heading {
    font-size: 1.3rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
}

.answer-box {
    background-color: #2e2e2e;
    color: #ffffff;
    padding: 1rem;
    border-radius: 6px;
    margin: 1rem 0;
    border: 1px solid #444;
}

.answer-title {
    font-weight: bold;
    margin-bottom: 0.5rem;
}

.st-button {
    margin: 0.5rem;
}

/* 
   Make sure the text content inside these boxes is 
   shown as plain text without rendering any HTML within it.
*/
.plain-text {
    white-space: pre-wrap;   /* preserve line breaks */
}
</style>
"""

st.markdown(BUBBLE_CSS, unsafe_allow_html=True)

# 3. Session State
if "selected_card" not in st.session_state:
    st.session_state.selected_card = None

if "show_answer" not in st.session_state:
    st.session_state.show_answer = False

# 4. Callbacks
def draw_topic():
    """Pick a random flashcard and reset answer state."""
    st.session_state.selected_card = random.choice(flashcards)
    st.session_state.show_answer = False

def show_answer():
    """Reveal the answer."""
    st.session_state.show_answer = True

# 5. Layout
st.title("AI Learning Capsules")

col1, col2 = st.columns(2)

with col1:
    st.button("Draw Topic", on_click=draw_topic)

with col2:
    st.button(
        "Show Answer",
        on_click=show_answer,
        disabled=(st.session_state.selected_card is None)
    )

# 6. Display the Q&A in the Styled Boxes
if st.session_state.selected_card:
    card_id = st.session_state.selected_card["id"]
    topic_text = st.session_state.selected_card["topic"]
    answer_text = st.session_state.selected_card["answer"]

    # -- Topic Bubble Layout --
    st.markdown(
        f"""
        <div class="question-box">
            <div class="question-heading">Topic no. {card_id}</div>
            <div class="plain-text">{topic_text}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # -- Answer Box (Only if "Show Answer" is clicked) --
    if st.session_state.show_answer:
        st.markdown(
            f"""
            <div class="answer-box">
                <div class="answer-title">Answer to Topic no. {card_id}</div>
                <div class="plain-text">{answer_text}</div>
            </div>
            """,
            unsafe_allow_html=True
        )