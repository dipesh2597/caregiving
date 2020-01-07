import mysql.connector
import register
import login


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
mycursor.execute("CREATE TABLE IF NOT EXISTS elders (PK_elder_id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), password VARCHAR(255), mobile VARCHAR(10) UNIQUE, younger_name VARCHAR(255), available BOOLEAN Default True, fund Integer, review VARCHAR(255), rating float)")
mycursor.execute("CREATE TABLE IF NOT EXISTS youngers (PK_younger_id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), password VARCHAR(255), mobile VARCHAR(10) UNIQUE, elders_name varchar(2555), review VARCHAR(255), rating float)")
# Request table for younger to elder
mycursor.execute("CREATE TABLE IF NOT EXISTS request (PK_request_id INT AUTO_INCREMENT PRIMARY KEY, younger_id integer, elder_id integer, request BOOLEAN Default False)")


# welcome note and giving oprion to login or register

def Welcome():
    print("Please select\n1. Login as Elder \n2. Login as Younger\n3. Register\n4. View all youngers who are taking care\n5. View all old couple with their care taker youngers name\n6. Exit")
    task = int(input())
    if task==1:
        mobile = input("Welcome Elder\nEnter Your Mobile Number: ")
        password = input("Enter Your Password: ")
        user = login.Elder_Login(mobile, password)
        user.login(mobile,password)
    
    elif task==2:
        mobile = input("Welcome younger\nEnter Your Mobile Number: ")
        password = input("Enter Your Password: ")
        user = login.Younger_Login(mobile, password)
        user.login(mobile,password)
    
    elif task==3:
        name = input("Register Yourselg\nEnter Your Full Name: ")
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
        user_signup = register.User_SignUp(name, password, mobile, role)
        user_signup.user_registration()
    
    elif task==4:
        sql = f'SELECT younger_name from elders WHERE mobile={mobile}'
        val=(mobile)
        mycursor.execute(sql, val)
        younger_name = mycursor.fetchone()
        sql=f'select name from elders where mobile={mobile}'
        val=(mobile)
        mycursor.execute(sql, val)
        elder_name = mycursor.fetchone()
        print(f'{younger_name[0]} is taking care of {elder_name[0]}.')
        pass
    elif task==5:
        sql = f'SELECT * from youngers'
        mycursor.execute(sql)
        younger_info = mycursor.fetchone()
        for i in range(len(younger_info)):
            if younger_info[i][4]!=None:
                print(f'{younger_info[1]}'')
        print("this all youngeFolks are taking care of some older")
        pass
    elif task==6:
        exit()

Welcome()
