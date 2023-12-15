import mysql.connector
import time

def create_connection():
    connection = mysql.connector.connect(
        user="root",
        password="123456",
        host="localhost"
    )

    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS railway")
    cursor.close()

    connection = mysql.connector.connect(
        user="root",
        password="123456",
        host="localhost",
        database="railway"
    )

    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            source VARCHAR(255) NOT NULL,
            destination VARCHAR(255) NOT NULL,
            date DATE NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    connection.commit()
    cursor.close()

    return connection

def user_login(connection, username, password):
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    cursor.close()
    return user

def book_ticket(connection, user_id, source, destination, date):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO tickets (user_id, source, destination, date) VALUES (%s, %s, %s, %s)",
                   (user_id, source, destination, date))
    connection.commit()
    cursor.close()
    print("Ticket booked successfully!")

def cancel_ticket(connection, ticket_id):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM tickets WHERE id = %s", (ticket_id,))
    connection.commit()
    cursor.close()
    print("Ticket canceled successfully!")

def view_tickets(connection, user_id):
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tickets WHERE user_id = %s", (user_id,))
    tickets = cursor.fetchall()
    cursor.close()

    if not tickets:
        print("No tickets booked.")
    else:
        print("\nTickets:")
        for ticket in tickets:
            print(f"Ticket ID: {ticket['id']}, Source: {ticket['source']}, Destination: {ticket['destination']}, Date: {ticket['date']}")

def main():
    connection = create_connection()

    while True:
        print("\nOptions:")
        print("1. Login")
        print("2. Book Ticket")
        print("3. Cancel Ticket")
        print("4. View Tickets")
        print("5. Exit")

        choice = input("Enter your choice (1/2/3/4/5): ")

        if choice == "1":
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            user = user_login(connection, username, password)

            if user:
                print("Login successful!")
                user_id = user['id']
            else:
                print("Login failed. Please try again.")
                continue

        elif choice == "2":
            source = input("Enter source station: ")
            destination = input("Enter destination station: ")
            date = input("Enter travel date (YYYY-MM-DD): ")
            book_ticket(connection, user_id, source, destination, date)

        elif choice == "3":
            try:
                ticket_id = int(input("Enter the Ticket ID to cancel: "))
                cancel_ticket(connection, ticket_id)
            except ValueError:
                print("Invalid input. Ticket ID must be a number.")

        elif choice == "4":
            view_tickets(connection, user_id)

        elif choice == "5":
            print("Exiting program.")
            break

        else:
            print("Invalid choice. Try again.")

    connection.close()

# Password login loop
while True:
    login = input("Enter password to unlock: ")
    if login == "123456":
        line = "Logging in, please wait..."
        words = line.split()
        for word in words:
            print(word, end=' ', flush=True)
            time.sleep(0.5)
        main()
        break
    else:
        print("Incorrect password. Try again.")
