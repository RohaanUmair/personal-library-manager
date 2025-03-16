import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin SDK
cred = credentials.Certificate("firebase-keys.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# Firestore reference
db = firestore.client()

# Function to add a book
def add_book(title, author, year, genre, read_status):
    book = {
        "title": title,
        "author": author,
        "year": year,
        "genre": genre,
        "read": read_status
    }
    db.collection("books").add(book)

# Function to remove a book
def remove_book(title):
    books_ref = db.collection("books")
    docs = books_ref.where("title", "==", title).stream()
    for doc in docs:
        doc.reference.delete()

# Function to search for books
def search_books(field, keyword):
    books_ref = db.collection("books")
    docs = books_ref.where(field, ">=", keyword).stream()
    return [doc.to_dict() for doc in docs]

# Function to display all books
def get_all_books():
    docs = db.collection("books").stream()
    return [doc.to_dict() for doc in docs]

# Function to display statistics
def get_statistics():
    docs = db.collection("books").stream()
    total_books = 0
    read_books = 0
    for doc in docs:
        book = doc.to_dict()
        total_books += 1
        if book['read']:
            read_books += 1
    percentage_read = (read_books / total_books) * 100 if total_books > 0 else 0
    return total_books, round(percentage_read, 1)

# Streamlit UI
st.title("📚 Firestore Book Manager")

menu = st.sidebar.selectbox("Menu", ["Add Book", "Remove Book", "Search Book", "Display All Books", "Statistics"])

if menu == "Add Book":
    with st.form("add_book_form"):
        title = st.text_input("Book Title")
        author = st.text_input("Author")
        year = st.text_input("Publication Year")
        genre = st.text_input("Genre")
        read_status = st.checkbox("Read")
        submit = st.form_submit_button("Add Book")
        if submit:
            add_book(title, author, year, genre, read_status)
            st.success("Book added successfully!")

elif menu == "Remove Book":
    book_title = st.text_input("Enter the title of the book to remove")
    if st.button("Remove Book"):
        remove_book(book_title)
        st.success("Book removed successfully!")

elif menu == "Search Book":
    search_option = st.radio("Search by", ["Title", "Author"])
    keyword = st.text_input("Enter keyword")
    if st.button("Search"):
        field = "title" if search_option == "Title" else "author"
        books = search_books(field, keyword)
        if books:
            for book in books:
                st.write(book)
        else:
            st.warning("No matching book found.")

elif menu == "Display All Books":
    books = get_all_books()
    if books:
        for book in books:
            st.write(book)
    else:
        st.warning("No books in the library.")

elif menu == "Statistics":
    total_books, percentage_read = get_statistics()
    st.write(f"Total Books: {total_books}")
    st.write(f"Percentage Read: {percentage_read}%")
