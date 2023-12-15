# Student management system with mysql
# connecting mysql 
import mysql.connector
import csv
connect=mysql.connector.connect(host='localhost',user='root',passwd='123456',charset='utf8')
cursor= connect.cursor()
# Create database if not exists
create_db_query = 'CREATE DATABASE IF NOT EXISTS student_data_manager'
cursor.execute(create_db_query)
connect.database = 'student_data_manager'

# Create table if not exists
create_table_query = '''
CREATE TABLE IF NOT EXISTS student_datas (
    name VARCHAR(100),
    address VARCHAR(100),
    phone VARCHAR(10),
    fname VARCHAR(100),
    mname VARCHAR(100),
    roll_no INT PRIMARY KEY
)
'''
cursor.execute(create_table_query)
connect.commit()
# student adding function

def add_sutdent():
    name=input("Enter Student Name : - ")
    address=input("Enter Student's Addresss : - ")
    phone=input("Enter Student's Phone number : - ")
    fname=input("Enter Student's Father Name : - ")
    mname=input("Enter Student's Mothers Name : - ")
    roll_no=int(input("Enter Student's Roll No. : - "))
    q1='insert into student_datas values(%s,%s,%s,%s,%s,%s)'
    data=(name,address,phone,fname,mname,roll_no)
    cursor.execute(q1,data)
    connect.commit()
    print("Data Enteres Succesfully ")

# student adding function end here

# student viewing function
def view_student():
    roll_no=int(input("Enter Roll Number of Student to search "))
    q2='select * from student_datas where roll_no = %s'
    data=(roll_no,)
    cursor.execute(q2,data)
    result=cursor.fetchone()
    if result:
        # Print or process the data here
        print("Student found:", result)
    else:
        print("Student not found.")
    connect.commit()

# sutdent viewing function end here
# student data deleting funtion

def delete_data():
    print("'NOTE :- data once deleted cannot be undo carefully go forward otherwise fill wrong roll_no '")
    roll_no=int(input("Enter roll number or enter 0"))
    qury='delete from student_datas where roll_no=%s'
    data=(roll_no)
    cursor.execute(qury,data)
    connect.commit()
    print("DATA DELETED THANK YOU ")

# student data deleting function end here

# student data updating function

def update_data():
    roll_no=int(input("Enter roll number of Student "))
    name=input("Enter name to update ")
    address=input("Enter address to update ")
    fname=input("Enter father name to update ")
    mname=input("Enter mother name to update ")
    print("NOTE :- 'Roll Number Cannot be updated '")
    query='update student_datas set name=%s,address=%s,fname=%s,mname=%s where roll_no=%s'
    data=(name,address,fname,mname,roll_no)
    print("DATA UPDATED THANK YOU ")
    updated_data="New value added "
    cursor.execute(query,(updated_data))
    connect.commit()


    # Function to save data to CSV
def save_to_csv():
    q2 = 'SELECT * FROM student_datas'
    cursor.execute(q2)
    results = cursor.fetchall()

    if results:
        headers = ["Name", "Address", "Phone", "Father Name", "Mother Name", "Roll No"]
        rows = [headers]

        for row in results:
            rows.append(row)

        with open('student_data.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
        print("Data exported to student_data.csv successfully.")

# update function end here  
# main function creating
def main():
    #creating student management main interface
    print("""
========================================
| Welcome to student management system |
========================================
| 1 . Add Student                      |
========================================
| 2 . View Student Data                |
========================================
| 3 . Update Student Data              |
========================================
| 4 . Delete Student Data              |
========================================
| 5 . Import to CSV                    |
=======================================
| 6 . Exit                             |
========================================
|    CHOOSE YOUR OPTION FROM ABOVE     |
========================================
          """)
    choice=int(input("Enter Your Option "))
    if choice==1:
        add_sutdent()
    elif choice==2:
        view_student()
    elif choice==3:
        update_data()
    elif choice==4:
        delete_data()
    elif choice==6:
        exit()
    elif choice==5:
        save_to_csv()
    else:
        print("Wrong Choice Plz Try Again ")
# main function end here
# connecting mysql succeed
while True:
    loggin=input("Enter password to unlock software for use :- ")
    if loggin=='123456':
        main()
    else:
        continue
