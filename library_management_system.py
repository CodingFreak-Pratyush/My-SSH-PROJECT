import csv
import mysql.connector

# Connect to MySQL without specifying a database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456"
)

# Create a cursor object
cursor = connection.cursor()

# Create the database if it doesn't exist
cursor.execute("CREATE DATABASE IF NOT EXISTS library_management_system")
cursor.execute("USE library_management_system")

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    quantity INT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT,
    user_id INT,
    checkout_date DATE,
    return_date DATE,
    FOREIGN KEY (book_id) REFERENCES books(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")


# Function to add a book to the library
def add_book(title, author, quantity):
    cursor.execute("INSERT INTO books (title, author, quantity) VALUES (%s, %s, %s)", (title, author, quantity))
    connection.commit()
    print(f"Book '{title}' by {author} added to the library.")

# Function to register a user
def add_user(name, email):
    cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
    connection.commit()
    print(f"User '{name}' registered.")

# Function to check out a book
def checkout_book(book_id, user_id):
    cursor.execute("INSERT INTO transactions (book_id, user_id, checkout_date) VALUES (%s, %s, CURDATE())", (book_id, user_id))
    cursor.execute("UPDATE books SET quantity = quantity - 1 WHERE id = %s", (book_id,))
    connection.commit()
    print(f"Book with ID {book_id} checked out by user with ID {user_id}.")

# Function to return a book
def return_book(transaction_id):
    cursor.execute("UPDATE transactions SET return_date = CURDATE() WHERE id = %s", (transaction_id,))
    transaction = cursor.execute("SELECT book_id FROM transactions WHERE id = %s", (transaction_id,))
    book_id = cursor.fetchone()[0]
    cursor.execute("UPDATE books SET quantity = quantity + 1 WHERE id = %s", (book_id,))
    connection.commit()
    print(f"Book returned for transaction with ID {transaction_id}.")

# Function to display available books
def display_available_books():
    cursor.execute("SELECT * FROM books WHERE quantity > 0")
    books = cursor.fetchall()
    if not books:
        print("No available books.")
    else:
        print("\nAvailable Books:")
        for book in books:
            print(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Quantity: {book[3]}")

# Function to list users
def list_users():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    if not users:
        print("No registered users.")
    else:
        print("\nRegistered Users:")
        for user in users:
            print(f"ID: {user[0]}, Name: {user[1]}, Email: {user[2]}")

# Function to view transaction history
def view_transaction_history():
    cursor.execute("SELECT * FROM transactions")
    transactions = cursor.fetchall()
    if not transactions:
        print("No transaction history.")
    else:
        print("\nTransaction History:")
        for transaction in transactions:
            print(f"Transaction ID: {transaction[0]}, Book ID: {transaction[1]}, User ID: {transaction[2]}, "
                  f"Checkout Date: {transaction[3]}, Return Date: {transaction[4]}")

# Function to display menu options
def display_menu():
    print("\nLibrary Management System Menu:")
    print("1. Add Book")
    print("2. Register User")
    print("3. Check Out Book")
    print("4. Return Book")
    print("5. Display Available Books")
    print("6. List Users")
    print("7. View Transaction History")
    print("8. Save Data to CSV")
    print("9. Exit")

# Function to get user input
def get_user_choice():
    return input("Enter your choice (1-9): ")

# Function to save data to CSV
def save_data_to_csv():
    with open('library_data.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        
        # Write header
        csv_writer.writerow(["Books"])
        csv_writer.writerow(["ID", "Title", "Author", "Quantity"])
        
        cursor.execute("SELECT * FROM books")
        books = cursor.fetchall()
        csv_writer.writerows(books)
        
        csv_writer.writerow([])  # Blank line between tables
        
        csv_writer.writerow(["Users"])
        csv_writer.writerow(["ID", "Name", "Email"])
        
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        csv_writer.writerows(users)
        
        csv_writer.writerow([])  # Blank line between tables
        
        csv_writer.writerow(["Transactions"])
        csv_writer.writerow(["ID", "Book ID", "User ID", "Checkout Date", "Return Date"])
        
        cursor.execute("SELECT * FROM transactions")
        transactions = cursor.fetchall()
        csv_writer.writerows(transactions)
        
    print("Data saved to 'library_data.csv'.")

# Example usage
while True:
    display_menu()
    choice = get_user_choice()

    if choice == '1':
        title = input("Enter the title of the book: ")
        author = input("Enter the author of the book: ")
        quantity = int(input("Enter the quantity of the book: "))
        add_book(title, author, quantity)

    elif choice == '2':
        name = input("Enter the name of the user: ")
        email = input("Enter the email of the user: ")
        add_user(name, email)

    elif choice == '3':
        book_id = int(input("Enter the ID of the book: "))
        user_id = int(input("Enter the ID of the user: "))
        checkout_book(book_id, user_id)

    elif choice == '4':
        transaction_id = int(input("Enter the ID of the transaction: "))
        return_book(transaction_id)

    elif choice == '5':
        display_available_books()

    elif choice == '6':
        list_users()

    elif choice == '7':
        view_transaction_history()

    elif choice == '8':
        save_data_to_csv()

    elif choice == '9':
        print("Exiting the Library Management System.")
        break

    else:
        print("Invalid choice. Please enter a number between 1 and 9.")

# Close the connection
cursor.close()
connection.close()
