import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin SDK
cred = credentials.Certificate("firebase-keys.json")
firebase_admin.initialize_app(cred)

# Firestore reference
db = firestore.client()


def add_book():
    title = input("Enter the book title: ")
    author = input("Enter the author: ")
    year = input("Enter the publication year: ")
    genre = input("Enter the genre: ")
    read_status = input("Have you read this book? (yes/no): ").strip().lower() == 'yes'

    book = {
        "title": title,
        "author": author,
        "year": year,
        "genre": genre,
        "read": read_status
    }

    db.collection("books").add(book)
    print("Book added successfully!")


def remove_book():
    title = input("Enter the title of the book to remove: ")
    books_ref = db.collection("books")
    docs = books_ref.where("title", "==", title).stream()

    found = False
    for doc in docs:
        doc.reference.delete()
        found = True

    if found:
        print("Book removed successfully!")
    else:
        print("Book not found.")


def search_book():
    print("Search by:\n1. Title\n2. Author")
    choice = input("Enter your choice: ")
    keyword = input("Enter the keyword: ").lower()

    books_ref = db.collection("books")
    if choice == '1':
        docs = books_ref.where("title", ">=", keyword).stream()
    elif choice == '2':
        docs = books_ref.where("author", ">=", keyword).stream()
    else:
        print("Invalid choice.")
        return

    found = False
    for doc in docs:
        book = doc.to_dict()
        status = 'Read' if book['read'] else 'Unread'
        print(book['title'], "by", book['author'], "(", book['year'], ") -", book['genre'], "-", status)
        found = True

    if not found:
        print("No matching book found.")


def display_all_books():
    docs = db.collection("books").stream()

    found = False
    for doc in docs:
        book = doc.to_dict()
        status = 'Read' if book['read'] else 'Unread'
        print(book['title'], "by", book['author'], "(", book['year'], ") -", book['genre'], "-", status)
        found = True

    if not found:
        print("No books in the library.")



def display_statistics():
    docs = db.collection("books").stream()

    total_books = 0
    read_books = 0

    for doc in docs:
        book = doc.to_dict()
        total_books += 1
        if book['read']:
            read_books += 1

    if total_books == 0:
        print("No books in the library.")
        return

    percentage_read = (read_books / total_books) * 100
    print("Total books:", total_books)
    print("Percentage read:", round(percentage_read, 1), "%")


def menu():
    while True:
        print("\nMenu")
        print("1. Add a book")
        print("2. Remove a book")
        print("3. Search for a book")
        print("4. Display all books")
        print("5. Display statistics")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_book()
        elif choice == '2':
            remove_book()
        elif choice == '3':
            search_book()
        elif choice == '4':
            display_all_books()
        elif choice == '5':
            display_statistics()
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


menu()