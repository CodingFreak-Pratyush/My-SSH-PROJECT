import mysql.connector

# Connect to MySQL
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    
)

# Create a cursor object to execute SQL queries
cursor = connection.cursor()


# Create the database if it does not exist
database_name = "flight_booking"
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
cursor.execute(f"USE {database_name}")


# Create tables if not exists
flight_table_query = """
CREATE TABLE IF NOT EXISTS flights (
    flight_id INT AUTO_INCREMENT PRIMARY KEY,
    flight_name VARCHAR(255) NOT NULL,
    source VARCHAR(255) NOT NULL,
    destination VARCHAR(255) NOT NULL,
    departure_date DATE NOT NULL,
    available_seats INT NOT NULL
)
"""

booking_table_query = """
CREATE TABLE IF NOT EXISTS bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    flight_id INT,
    passenger_name VARCHAR(255) NOT NULL,
    seat_number INT NOT NULL,
    FOREIGN KEY (flight_id) REFERENCES flights(flight_id)
)
"""

cursor.execute(flight_table_query)
cursor.execute(booking_table_query)

# Function to display available flights
def display_flights():
    query = "SELECT * FROM flights"
    cursor.execute(query)
    flights = cursor.fetchall()
    print("\nAvailable Flights:")
    print("ID | Flight Name | Source | Destination | Departure Date | Available Seats")
    print("-" * 80)
    for flight in flights:
        print(f"{flight[0]} | {flight[1]} | {flight[2]} | {flight[3]} | {flight[4]} | {flight[5]}")

def book_flight(flight_id, passenger_name, seat_number):
    query = "SELECT * FROM flights WHERE flight_id = %s AND available_seats > 0"
    cursor.execute(query, (flight_id,))
    flight = cursor.fetchone()

    if flight:
        update_query = "UPDATE flights SET available_seats = available_seats - 1 WHERE flight_id = %s"
        cursor.execute(update_query, (flight_id,))

        insert_query = "INSERT INTO bookings (flight_id, passenger_name, seat_number) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (flight_id, passenger_name, seat_number))

        connection.commit()
        print("\nBooking successful!")
    else:
        print("\nFlight not available or no seats left.")


# Function to display available flights
def display_flights():
    query = "SELECT * FROM flights"
    cursor.execute(query)
    flights = cursor.fetchall()
    print("\nAvailable Flights:")
    print("ID | Flight Name | Source | Destination | Departure Date | Available Seats")
    print("-" * 80)
    for flight in flights:
        print(f"{flight[0]} | {flight[1]} | {flight[2]} | {flight[3]} | {flight[4]} | {flight[5]}")

# Function to add a new flight
def add_flight():
    flight_name = input("Enter Flight Name: ")
    source = input("Enter Source: ")
    destination = input("Enter Destination: ")
    departure_date = input("Enter Departure Date (YYYY-MM-DD): ")
    available_seats = int(input("Enter Available Seats: "))

    insert_query = "INSERT INTO flights (flight_name, source, destination, departure_date, available_seats) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(insert_query, (flight_name, source, destination, departure_date, available_seats))

    connection.commit()
    print("\nFlight added successfully!")

# Main menu
while True:
    print("\nFlight Ticket Booking Management System")
    print("1. Display Available Flights")
    print("2. Book a Flight")
    print("3. Add a New Flight")
    print("4. Exit")

    choice = input("Enter your choice (1/2/3/4): ")

    if choice == "1":
        display_flights()
    elif choice == "2":
        flight_id = input("Enter Flight ID: ")
        passenger_name = input("Enter Passenger Name: ")
        seat_number = input("Enter Seat Number: ")
        book_flight(int(flight_id), passenger_name, int(seat_number))
    elif choice == "3":
        add_flight()
    elif choice == "4":
        break
    else:
        print("Invalid choice. Please enter 1, 2, 3, or 4.")
# Close the connection
cursor.close()
connection.close()
