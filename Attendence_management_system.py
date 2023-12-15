import mysql.connector
from datetime import date
import csv

# Connect to MySQL Database and Create if Not Exist
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456"
        )
        cursor = connection.cursor()

        # Create database if not exists
        cursor.execute("CREATE DATABASE IF NOT EXISTS your_database")
        print("Connected to the database!")

        # Switch to the specified database
        cursor.execute("USE your_database")

        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Create Attendance Table
def create_attendance_table(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS attendance (
                id INT AUTO_INCREMENT PRIMARY KEY,
                student_id INT,
                date DATE,
                status VARCHAR(10)
            )
        """)
        print("Attendance table created successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()

# Mark Attendance
def mark_attendance(connection, student_id, status):
    cursor = connection.cursor()
    try:
        today = date.today()
        cursor.execute("""
            INSERT INTO attendance (student_id, date, status)
            VALUES (%s, %s, %s)
        """, (student_id, today, status))
        connection.commit()
        print(f"Attendance marked for student {student_id} with status {status}")
    except mysql.connector.Error as err:
        connection.rollback()
        print(f"Error: {err}")
    finally:
        cursor.close()

# Update Attendance
def update_attendance(connection, student_id, date, new_status):
    cursor = connection.cursor()
    try:
        cursor.execute("""
            UPDATE attendance
            SET status = %s
            WHERE student_id = %s AND date = %s
        """, (new_status, student_id, date))
        connection.commit()
        print(f"Attendance updated for student {student_id} on {date}. New status: {new_status}")
    except mysql.connector.Error as err:
        connection.rollback()
        print(f"Error: {err}")
    finally:
        cursor.close()

# View Attendance
def view_attendance(connection, student_id):
    cursor = connection.cursor()
    try:
        cursor.execute("""
            SELECT * FROM attendance
            WHERE student_id = %s
        """, (student_id,))
        rows = cursor.fetchall()

        if not rows:
            print(f"No attendance records found for student {student_id}")
        else:
            print(f"Attendance records for student {student_id}:")
            for row in rows:
                print(f"ID: {row[0]}, Date: {row[2]}, Status: {row[3]}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()

# View Attendance Report
def view_attendance_report(connection, student_id=None, start_date=None, end_date=None):
    cursor = connection.cursor()
    try:
        query = """
            SELECT * FROM attendance
        """
        params = ()
        
        if student_id is not None:
            query += " WHERE student_id = %s"
            params = (student_id,)
        elif start_date is not None and end_date is not None:
            query += " WHERE date BETWEEN %s AND %s"
            params = (start_date, end_date)

        cursor.execute(query, params)
        rows = cursor.fetchall()

        if not rows:
            print("No attendance records found.")
        else:
            print("Attendance Report:")
            for row in rows:
                print(f"ID: {row[0]}, Student ID: {row[1]}, Date: {row[2]}, Status: {row[3]}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()

# Export Attendance to CSV
def export_to_csv(connection, filename):
    cursor = connection.cursor()
    try:
        cursor.execute("""
            SELECT * FROM attendance
        """)
        rows = cursor.fetchall()

        if not rows:
            print("No attendance records to export.")
        else:
            header = ["ID", "Student ID", "Date", "Status"]

            with open(filename, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(header)
                csv_writer.writerows(rows)

            print(f"Attendance data exported to {filename}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()

# Main Function
def main():
    connection = connect_to_database()
    if connection:
        create_attendance_table(connection)

        while True:
            print("\nAttendance Management System:")
            print("1. Mark Attendance")
            print("2. Update Attendance")
            print("3. View Attendance")
            print("4. View Attendance Report")
            print("5. Export Attendance to CSV")
            print("6. Exit")

            choice = input("Enter your choice (1/2/3/4/5/6): ")

            if choice == '1':
                student_id = int(input("Enter student ID: "))
                status = input("Enter attendance status (Present/Absent): ").capitalize()
                mark_attendance(connection, student_id, status)
            elif choice == '2':
                student_id = int(input("Enter student ID: "))
                date = input("Enter date (YYYY-MM-DD): ")
                new_status = input("Enter new attendance status (Present/Absent): ").capitalize()
                update_attendance(connection, student_id, date, new_status)
            elif choice == '3':
                student_id = int(input("Enter student ID: "))
                view_attendance(connection, student_id)
            elif choice == '4':
                view_choice = input("View attendance report by (S)tudent ID or (D)ate range? ").upper()
                if view_choice == 'S':
                    student_id = int(input("Enter student ID: "))
                    view_attendance_report(connection, student_id=student_id)
                elif view_choice == 'D':
                    start_date = input("Enter start date (YYYY-MM-DD): ")
                    end_date = input("Enter end date (YYYY-MM-DD): ")
                    view_attendance_report(connection, start_date=start_date, end_date=end_date)
                else:
                    print("Invalid choice.")
            elif choice == '5':
                filename = input("Enter CSV file name: ")
                export_to_csv(connection, filename)
            elif choice == '6':
                break
            else:
                print("Invalid choice. Please enter 1, 2, 3, 4, 5, or 6.")

        connection.close()
        print("Connection closed. Exiting program.")

if __name__ == "__main__":
    main()
