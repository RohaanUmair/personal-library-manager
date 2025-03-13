books = []

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
    books.append(book)
    print("Book added successfully!")


def remove_book():
    title = input("Enter the title of the book to remove: ")
    index = 0
    while index < len(books):
        if books[index]['title'].lower() == title.lower():
            del books[index]
            print("Book removed successfully!")
            return
        index += 1
    print("Book not found.")


def search_book():
    print("Search by:\n1. Title\n2. Author")
    choice = input("Enter your choice: ")
    keyword = input("Enter the keyword: ").lower()
    found = False

    for book in books:
        if (choice == '1' and keyword in book['title'].lower()) or (choice == '2' and keyword in book['author'].lower()):
            status = 'Read' if book['read'] else 'Unread'
            print(book['title'], "by", book['author'], "(", book['year'], ") -", book['genre'], "-", status)
            found = True

    if not found:
        print("No matching book found.")


def display_all_books():
    if len(books) == 0:
        print("No books in the library.")
    else:
        for book in books:
            status = 'Read' if book['read'] else 'Unread'
            print(book['title'], "by", book['author'], "(", book['year'], ") -", book['genre'], "-", status)


def display_statistics():
    total_books = len(books)
    if total_books == 0:
        print("No books in the library.")
        return

    read_books = 0
    for book in books:
        if book['read']:
            read_books += 1

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
