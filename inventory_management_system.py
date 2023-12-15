import mysql.connector
import time

# Connect to MySQL database
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="inventory_management_system"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Create the database if not exists
def create_database(cursor, database_name):
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")



# Create the inventory table
def create_inventory_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INT AUTO_INCREMENT PRIMARY KEY,
            product_name VARCHAR(255) NOT NULL,
            quantity INT NOT NULL
        )
    """)

# Add an item to the inventory
def add_item(cursor, product_name, quantity):
    cursor.execute("INSERT INTO inventory (product_name, quantity) VALUES (%s, %s)", (product_name, quantity))

# Update quantity of an item in the inventory
def update_quantity(cursor, product_name, new_quantity):
    cursor.execute("UPDATE inventory SET quantity = %s WHERE product_name = %s", (new_quantity, product_name))

# Retrieve the inventory list
def get_inventory_list(cursor):
    cursor.execute("SELECT * FROM inventory")
    return cursor.fetchall()

# Main function
def main():
    connection = connect_to_database()

    if connection:
        cursor = connection.cursor()

        # Create the inventory table if not exists
        create_inventory_table(cursor)

        while True:
            print("\n1. Add item to inventory")
            print("2. Update quantity")
            print("3. View inventory")
            print("4. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                product_name = input("Enter product name: ")
                quantity = int(input("Enter quantity: "))
                add_item(cursor, product_name, quantity)
                connection.commit()
                print("Item added to inventory.")

            elif choice == "2":
                product_name = input("Enter product name: ")
                new_quantity = int(input("Enter new quantity: "))
                update_quantity(cursor, product_name, new_quantity)
                connection.commit()
                print("Quantity updated.")

            elif choice == "3":
                inventory_list = get_inventory_list(cursor)
                print("\nInventory List:")
                for item in inventory_list:
                    print(f"ID: {item[0]}, Product: {item[1]}, Quantity: {item[2]}")

            elif choice == "4":
                break

            else:
                print("Invalid choice. Please try again.")

        # Close the cursor and connection
        cursor.close()
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

