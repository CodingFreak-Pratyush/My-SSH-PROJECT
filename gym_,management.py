import mysql.connector
from datetime import timedelta, datetime
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456"
)
cursor = connection.cursor()

database_name = "gym_management"
cursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(database_name))
connection.database = database_name

cursor.execute("""
    CREATE TABLE IF NOT EXISTS members (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        email VARCHAR(255),
        phone VARCHAR(15),
        membership_start DATE,
        membership_end DATE
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS workouts (
        id INT AUTO_INCREMENT PRIMARY KEY,
        member_id INT,
        workout_date DATE,
        duration_minutes INT,
        FOREIGN KEY (member_id) REFERENCES members(id)
    )
""")

def add_member(name, email, phone, membership_start, membership_duration):
    membership_end = membership_start + timedelta(days=membership_duration)
    sql = "INSERT INTO members (name, email, phone, membership_start, membership_end) VALUES (%s, %s, %s, %s, %s)"
    values = (name, email, phone, membership_start, membership_end)
    cursor.execute(sql, values)
    connection.commit()
    print("Member added successfully!")

def log_workout(member_id, workout_date, duration_minutes):
    sql = "INSERT INTO workouts (member_id, workout_date, duration_minutes) VALUES (%s, %s, %s)"
    values = (member_id, workout_date, duration_minutes)
    cursor.execute(sql, values)
    connection.commit()
    print("Workout logged successfully!")

def view_workout_history(member_id):
    sql = "SELECT * FROM workouts WHERE member_id = %s"
    cursor.execute(sql, (member_id,))
    workouts = cursor.fetchall()
    if not workouts:
        print("No workout history found for this member.")
    else:
        print("Workout history for Member ID {}: ".format(member_id))
        for workout in workouts:
            print("Workout ID: {}, Date: {}, Duration: {} minutes".format(workout[0], workout[2], workout[3]))

def list_all_members():
    sql = "SELECT * FROM members"
    cursor.execute(sql)
    members = cursor.fetchall()
    if not members:
        print("No members found.")
    else:
        print("List of all members:")
        for member in members:
            print("Member ID: {}, Name: {}, Email: {}, Phone: {}".format(member[0], member[1], member[2], member[3]))

while True:
    print("\n1. Add Member\n2. Remove Member\n3. Log Workout\n4. View Workout History\n5. List All Members\n6. Exit")
    choice = input("Enter your choice (1-6): ")

    if choice == "1":
        name = input("Enter member name: ")
        email = input("Enter member email: ")
        phone = input("Enter member phone: ")
        duration = int(input("Enter membership duration (in days): "))
        add_member(name, email, phone, datetime.now())
    elif choice == "2":
        remove_member()
    elif choice == "3":
        log_workout()
    elif choice == "4":
        view_workout_history()
    elif choice == "5":
        list_all_members()
    elif choice == "6":
        break
    else:
        print("Invalid choice. Please enter a number between 1 and 6.")