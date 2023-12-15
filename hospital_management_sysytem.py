import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    
)

cursor = connection.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS hospital_management_system")
cursor.execute("USE hospital_management_system")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Patients (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        age INT,
        gender VARCHAR(10),
        admission_date DATE,
        discharge_date DATE
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Doctors (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        specialization VARCHAR(255)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS PatientDoctor (
        patient_id INT,
        doctor_id INT,
        PRIMARY KEY (patient_id, doctor_id),
        FOREIGN KEY (patient_id) REFERENCES Patients(id),
        FOREIGN KEY (doctor_id) REFERENCES Doctors(id)
    )
""")

def add_patient(name, age, gender, admission_date, discharge_date):
    cursor.execute("""
        INSERT INTO Patients (name, age, gender, admission_date, discharge_date)
        VALUES (%s, %s, %s, %s, %s)
    """, (name, age, gender, admission_date, discharge_date))
    connection.commit()

def add_doctor(name, specialization):
    cursor.execute("""
        INSERT INTO Doctors (name, specialization)
        VALUES (%s, %s)
    """, (name, specialization))
    connection.commit()

def assign_doctor_to_patient(patient_id, doctor_id):
    cursor.execute("""
        INSERT INTO PatientDoctor (patient_id, doctor_id)
        VALUES (%s, %s)
    """, (patient_id, doctor_id))
    connection.commit()

def get_all_patients():
    cursor.execute("SELECT * FROM Patients")
    return cursor.fetchall()

def get_all_doctors():
    cursor.execute("SELECT * FROM Doctors")
    return cursor.fetchall()

def get_patient_doctor_assignments():
    cursor.execute("""
        SELECT Patients.name as patient_name, Doctors.name as doctor_name
        FROM PatientDoctor
        JOIN Patients ON PatientDoctor.patient_id = Patients.id
        JOIN Doctors ON PatientDoctor.doctor_id = Doctors.id
    """)
    return cursor.fetchall()

def display_patients():
    patients = get_all_patients()
    print("\nPatients:")
    for patient in patients:
        print(patient)

def display_doctors():
    doctors = get_all_doctors()
    print("\nDoctors:")
    for doctor in doctors:
        print(doctor)

def display_patient_doctor_assignments():
    assignments = get_patient_doctor_assignments()
    print("\nPatient-Doctor Assignments:")
    for assignment in assignments:
        print(f"{assignment[0]} - {assignment[1]}")

def main_menu():
    while True:
        print("\nHospital Management System Menu:")
        print("1. Add Patient")
        print("2. Add Doctor")
        print("3. Assign Doctor to Patient")
        print("4. Display Patients")
        print("5. Display Doctors")
        print("6. Display Patient-Doctor Assignments")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ")

        if choice == "1":
            name = input("Enter patient name: ")
            age = int(input("Enter patient age: "))
            gender = input("Enter patient gender: ")
            admission_date = input("Enter admission date (YYYY-MM-DD): ")
            discharge_date = input("Enter discharge date (YYYY-MM-DD): ")
            add_patient(name, age, gender, admission_date, discharge_date)
        elif choice == "2":
            name = input("Enter doctor name: ")
            specialization = input("Enter doctor specialization: ")
            add_doctor(name, specialization)
        elif choice == "3":
            display_patients()
            patient_id = int(input("Enter patient ID to assign a doctor: "))
            display_doctors()
            doctor_id = int(input("Enter doctor ID to assign to the patient: "))
            assign_doctor_to_patient(patient_id, doctor_id)
        elif choice == "4":
            display_patients()
        elif choice == "5":
            display_doctors()
        elif choice == "6":
            display_patient_doctor_assignments()
        elif choice == "7":
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")

if __name__ == "__main__":
    main_menu()

cursor.close()
connection.close()
