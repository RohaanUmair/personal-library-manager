import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin SDK with singleton pattern
def initialize_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate("firebase-keys.json")
        firebase_admin.initialize_app(cred)
    return firestore.client()

@st.cache_resource
def get_firestore_db():
    return initialize_firebase()

db = get_firestore_db()

# Rest of the code remains the same as previous answer...

def add_book():
    st.header("Add a Book")
    with st.form("add_book_form"):
        title = st.text_input("Title")
        author = st.text_input("Author")
        year = st.text_input("Publication Year")
        genre = st.text_input("Genre")
        read_status = st.checkbox("Read Status")
        submitted = st.form_submit_button("Add Book")
        
        if submitted:
            if title and author:  # Basic validation
                book = {
                    "title": title,
                    "author": author,
                    "year": year,
                    "genre": genre,
                    "read": read_status
                }
                db.collection("books").add(book)
                st.success("Book added successfully!")
            else:
                st.warning("Title and Author are required fields")

def remove_book():
    st.header("Remove a Book")
    title = st.text_input("Enter title to remove")
    if st.button("Remove Book"):
        if title:
            books_ref = db.collection("books")
            docs = books_ref.where("title", "==", title).stream()
            
            found = False
            for doc in docs:
                doc.reference.delete()
                found = True
            
            if found:
                st.success("Book removed successfully!")
            else:
                st.error("Book not found")
        else:
            st.warning("Please enter a title")

def search_book():
    st.header("Search Books")
    search_type = st.radio("Search by", ["Title", "Author"])
    keyword = st.text_input("Enter search keyword").lower()
    
    if st.button("Search"):
        if keyword:
            books_ref = db.collection("books")
            if search_type == "Title":
                docs = books_ref.where("title", ">=", keyword).stream()
            else:
                docs = books_ref.where("author", ">=", keyword).stream()
            
            books = []
            for doc in docs:
                book = doc.to_dict()
                book["status"] = 'Read' if book['read'] else 'Unread'
                books.append(book)
            
            if books:
                st.dataframe(books)
            else:
                st.info("No matching books found")
        else:
            st.warning("Please enter a search keyword")

def display_all_books():
    st.header("All Books")
    docs = db.collection("books").stream()
    
    books = []
    for doc in docs:
        book = doc.to_dict()
        book["status"] = 'Read' if book['read'] else 'Unread'
        books.append(book)
    
    if books:
        st.dataframe(books)
    else:
        st.info("No books in the library")

def display_statistics():
    st.header("Library Statistics")
    docs = db.collection("books").stream()
    
    total_books = 0
    read_books = 0
    
    for doc in docs:
        book = doc.to_dict()
        total_books += 1
        if book['read']:
            read_books += 1
    
    if total_books == 0:
        st.info("No books in the library")
        return
    
    percentage_read = (read_books / total_books) * 100
    st.metric("Total Books", total_books)
    st.metric("Percentage Read", f"{percentage_read:.1f}%")

def main():
    st.title("📚 Book Library Manager")
    
    # Sidebar navigation
    menu_options = {
        "Add a book": add_book,
        "Remove a book": remove_book,
        "Search for a book": search_book,
        "Display all books": display_all_books,
        "Display statistics": display_statistics
    }
    
    selected = st.sidebar.selectbox("Menu", list(menu_options.keys()))
    
    # Display selected page
    menu_options[selected]()

if __name__ == "__main__":
    main()