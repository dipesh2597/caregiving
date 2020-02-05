import mysql.connector

# conneting mysql
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="password",
    use_pure=True,
)
cursor = mydb.cursor()

# creating database if not exists
cursor.execute("CREATE DATABASE IF NOT EXISTS caregiving")

# getting database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="password",
  use_pure=True,
  database="caregiving"
)
mycursor = mydb.cursor()

# creating tables for elder and younger if not exists
mycursor.execute("CREATE TABLE IF NOT EXISTS youngers (PK_younger_id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), password VARCHAR(255), mobile VARCHAR(10) UNIQUE, review VARCHAR(255), rating float)")
mycursor.execute("CREATE TABLE IF NOT EXISTS elders (PK_elder_id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), password VARCHAR(255), mobile VARCHAR(10) UNIQUE, FK_younger_ID Integer references youngers(PK_younger_id), available BOOLEAN Default True, fund Integer, review VARCHAR(255), rating float)")

# Request table for younger to elder
mycursor.execute("CREATE TABLE IF NOT EXISTS request (PK_request_id INT AUTO_INCREMENT PRIMARY KEY, FK_younger_id integer references youngers(PK_younger_id), FK_elder_id integer references elders(PK_elder_id), request_status BOOLEAN Default False)")

# import after creating database if does not exist because we required database in imported files if do will not create it before import then it will throw an error
from profile import User_SignUp
from younger_profile import Younger_Profile
from elder_profile import Elder_Profile

# welcome note and giving oprion to login or register
def Welcome():
    print("Please select\n1. Login as Elder \n2. Login as Younger\n3. Register\n4. View all youngers who are taking care\n5. View who is taking care of older couple\n6. Exit")
    task = int(input())
    if task==1:
        mobile = input("Welcome Elder\nEnter Your Mobile Number: ")
        password = input("Enter Your Password: ")
        user = Elder_Profile(mobile, password)
        user.login(mobile,password)
    
    elif task==2:
        mobile = input("Welcome younger\nEnter Your Mobile Number: ")
        password = input("Enter Your Password: ")
        user = Younger_Profile(mobile, password)
        user.login(mobile,password)
    
    elif task==3:
        name = input("Register Yourself\nEnter Your Full Name: ")
        mobile = input("Enter Your Mobile Number: ")
        password = input("Enter Your Password: ")
        # if a user select wrong option it will ask again to select option
        while True:
            role = int(input("select your role:\n1. Elder\n2. Younger\n"))
            try:
                if role==1:
                    role="elder"
                    break
                elif role==2:
                    role="younger"
                    break
            except:
                print(f'option not Valid! Please try again')
        user_signup = User_SignUp(name, password, mobile, role)
        user_signup.user_registration()
    
    elif task==4:
        sql = f'SELECT * from youngers where PK_younger_id in (select FK_younger_ID from elders)'
        mycursor.execute(sql)
        younger_info = mycursor.fetchall()
        print("This all youngeFolks are taking care of some older")
        for i in range(len(younger_info)):
            print(f'{i+1}. {younger_info[i][1]}')

    elif task==5:
        elderNumber = int(input("Please enter elder's mobile number.\n"))
        sql = f'SELECT name, FK_younger_id from elders WHERE mobile={elderNumber}'
        val=(elderNumber)
        mycursor.execute(sql, val)
        elder_detail= mycursor.fetchone()
        sql=f'select name from youngers where PK_younger_id={elder_detail[1]}'
        val=(elder_detail[0])
        mycursor.execute(sql, val)
        younger_name = mycursor.fetchone()
        print(f'{younger_name[0]} is taking care of {elder_detail[0]}.')
    elif task==6:
        exit()

Welcome()
