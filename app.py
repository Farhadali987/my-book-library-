import json
import streamlit as st
from time import sleep

# File to store book data
STORAGE_FILE = "books_data.json"

def load_books():
    try:
        with open(STORAGE_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_books(book_list):
    with open(STORAGE_FILE, "w") as file:
        json.dump(book_list, file, indent=4)

def add_book(title, author, year, genre, read):
    books = load_books()
    books.append({"title": title, "author": author, "year": year, "genre": genre, "read": read})
    save_books(books)

def delete_book(title):
    books = load_books()
    books = [book for book in books if book["title"].lower() != title.lower()]
    save_books(books)

def update_book(old_title, new_title, author, year, genre, read):
    books = load_books()
    for book in books:
        if book["title"].lower() == old_title.lower():
            book["title"] = new_title or book["title"]
            book["author"] = author or book["author"]
            book["year"] = year or book["year"]
            book["genre"] = genre or book["genre"]
            book["read"] = read
            break
    save_books(books)

def search_books(query):
    books = load_books()
    return [book for book in books if query.lower() in book["title"].lower() or query.lower() in book["author"].lower()]

def get_reading_progress():
    books = load_books()
    total_books = len(books)
    read_books = sum(1 for book in books if book["read"])
    return total_books, read_books, (read_books / total_books * 100) if total_books > 0 else 0

# Streamlit UI with animations
st.set_page_config(page_title="📚 Book Collection Manager", layout="centered")
st.title("📖 Book Collection Manager")

with st.sidebar:
    st.image("https://source.unsplash.com/400x300/?books", use_column_width=True)
    choice = st.radio("Navigation", ["Add Book", "View Books", "Search Book", "Update Book", "Delete Book", "Reading Progress"])

if choice == "Add Book":
    st.header("📚 Add a New Book")
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    year = st.text_input("Publication Year")
    genre = st.text_input("Genre")
    read = st.checkbox("Have you read this book?")
    if st.button("Add Book", help="Click to save the book", use_container_width=True):
        add_book(title, author, year, genre, read)
        st.success("Book added successfully!")
        sleep(1)
        st.rerun()

elif choice == "View Books":
    st.header("📖 Your Book Collection")
    books = load_books()
    if books:
        for book in books:
            st.markdown(f"### {book['title']} ({book['year']})")
            st.text(f"Author: {book['author']} | Genre: {book['genre']} | {'✅ Read' if book['read'] else '❌ Not Read'}")
            st.markdown("---")
    else:
        st.warning("No books found. Add some!")

elif choice == "Search Book":
    st.header("🔍 Search for a Book")
    query = st.text_input("Enter book title or author")
    if st.button("Search", use_container_width=True):
        results = search_books(query)
        if results:
            for book in results:
                st.markdown(f"### {book['title']} ({book['year']})")
                st.text(f"Author: {book['author']} | Genre: {book['genre']} | {'✅ Read' if book['read'] else '❌ Not Read'}")
        else:
            st.error("No books found.")

elif choice == "Update Book":
    st.header("✏️ Update Book Details")
    old_title = st.text_input("Enter the book title to update")
    new_title = st.text_input("New Title")
    author = st.text_input("New Author")
    year = st.text_input("New Publication Year")
    genre = st.text_input("New Genre")
    read = st.checkbox("Mark as Read?")
    if st.button("Update Book", use_container_width=True):
        update_book(old_title, new_title, author, year, genre, read)
        st.success("Book updated successfully!")
        sleep(1)
        st.rerun()

elif choice == "Delete Book":
    st.header("🗑️ Remove a Book")
    title = st.text_input("Enter book title to remove")
    if st.button("Delete", use_container_width=True):
        delete_book(title)
        st.warning("Book deleted!")
        sleep(1)
        st.rerun()

elif choice == "Reading Progress":
    st.header("📊 Reading Progress")
    total, read, progress = get_reading_progress()
    st.write(f"Total Books: {total}")
    st.write(f"Books Read: {read}")
    st.progress(progress / 100)
    st.write(f"Progress: {progress:.2f}%")

st.sidebar.markdown("---")
st.sidebar.write("📌 Manage your book collection with ease!")

st.markdown("<h5 style='text-align: center; color: gray;'>Developed by Farhad Gul</h5>", unsafe_allow_html=True)
