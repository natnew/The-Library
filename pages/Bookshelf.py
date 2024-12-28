import streamlit as st
import os
import json

# Set the page configuration
st.set_page_config(page_title="The Library - Bookshelf", layout="wide")

# Import other necessary libraries
import json
import os
from PIL import Image

# Function to load book data from a JSON file
def load_books():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(script_dir, '..', 'data', 'books.json')
        with open(json_path, 'r') as file:
            books = json.load(file)
        return books
    except FileNotFoundError:
        st.error(f"Error: The file {json_path} was not found.")
        return []
    except json.JSONDecodeError:
        st.error(f"Error: The file {json_path} contains invalid JSON.")
        return []

# Load books
books = load_books()

# Sort books alphabetically by title
books = sorted(books, key=lambda x: x['title'])

st.title("📚 The Library: Bookshelf")
st.write("Explore our curated collection of AI literature.")

# Function to display a single book entry
def display_book(book):
    # Display book cover
    if os.path.exists(book['cover_path']):
        image = Image.open(book['cover_path'])
        st.image(image, use_column_width=True)
    else:
        st.image("https://via.placeholder.com/150", use_column_width=True)

    # Display book title
    st.write(f"**{book['title']}**")

    # Display book description
    st.write(f"*{book['description']}*")

# Display books in a responsive grid
num_columns = 5  # Adjust the number of columns as needed
for i in range(0, len(books), num_columns):
    cols = st.columns(num_columns)
    for col, book in zip(cols, books[i:i + num_columns]):
        with col:
            display_book(book)
