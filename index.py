from db import *
from profile import User
from younger_profile import YoungerProfile
from elder_profile import ElderProfile

# welcome note and giving oprion to login or register
def welcome():
    print("Please select\n1. Login as Elder \n2. Login as Younger\n3. Register\n4. View all youngers who are taking care\n5. View who is taking care of older couple\n6. Exit")
    task = int(input())
    if task==1:
        mobile = input("Welcome Elder\nEnter Your Email: ")
        password = input("Enter Your Password: ")
        user = ElderProfile(mobile, password)
        user.log_in()
    
    elif task==2:
        mobile = input("Welcome younger\nEnter Your Email: ")
        password = input("Enter Your Password: ")
        user = YoungerProfile(mobile, password)
        user.log_in()
    
    elif task==3:
        name = input("Register Yourself\nEnter Your Full Name: ")
        email = input("Enter your email: ")
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

        user_signup = User(name, email, password, mobile, role)
        user_signup.user_registration()
        
    
    elif task==4:
        sql = f'SELECT name from users where PK_user_id in (select FK_younger_ID from elders)'
        mycursor.execute(sql)
        younger_info = mycursor.fetchall()
        print(younger_info)
        print("This all youngeFolks are taking care of some older")
        for i in range(len(younger_info)):
            print(f'{i+1}. {younger_info[i][0]}')
        welcome()

    elif task==5:
        elder_number = int(input("Please enter elder's mobile number.\n"))
        sql = f'SELECT PK_user_id from users where mobile={elder_number}'
        mycursor.execute(sql)
        user_id = mycursor.fetchone()
        sql = f'SELECT FK_younger_id, available from elders WHERE FK_user_id={user_id[0]}'
        mycursor.execute(sql)
        elder_detail= mycursor.fetchone()
        print(elder_detail)
        if elder_detail[1]==0:
            sql=f'select name from users where PK_user_id={elder_detail[0]}'
            val=(elder_detail[0])
            mycursor.execute(sql, val)
            younger_name = mycursor.fetchone()
            print(f'{younger_name[0]} is taking care of {elder_detail[0]}.')
        else:
            print(f'No one is taking care of {elder_detail[0]}')
        welcome()
    elif task==6:
        exit()

welcome()
