import mysql.connector
import younger_profile




mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="password",
  use_pure=True,
  database="caregiving"
)

mycursor = mydb.cursor()

# user registration class
class User_SignUp:
    #constructors
    def __init__(self, name, password, mobile, role):
        self.name = name
        self.password = password
        self.mobile = mobile
        self.role = role

    def user_registration(self):
        #retrieving all registered mobile no from both table
        sql = f'SELECT * FROM elders WHERE mobile= {self.mobile}'
        mycursor.execute(sql)
        elders_mobile_no = mycursor.fetchall()
        sql = f'SELECT * FROM youngers WHERE mobile= {self.mobile}'
        mycursor.execute(sql)
        youngers_mobile_no = mycursor.fetchall()
        
        if youngers_mobile_no==[] and elders_mobile_no==[]:    
            if self.role=='elder':
                sql = "INSERT INTO elders (name, password, mobile) VALUES (%s, %s, %s)"
                val = (self.name, self.password, self.mobile)
                mycursor.execute(sql, val)
                mydb.commit()
                print(f'Account Created for {self.name}')
                import elder_profile
                elder = elder_profile.Elder_Profile(self.mobile)
                elder.Dashboard_elder()
            elif self.role=='younger':
                sql = "INSERT INTO youngers (name, password, mobile) VALUES (%s, %s, %s)"
                val = (self.name, self.password, self.mobile)
                mycursor.execute(sql, val)
                mydb.commit()
                print(f'Account Created for {self.name}')
                young = younger_profile.Younger_Profile(self.mobile)
                young.Dashboard_younger()


        # if no already registered ask them to login again or reset password
        else:  # fetchall stores tuple in a list
            print(f'Account already created for {self.mobile} Please try to Login using your mobile number and password.\n Want to reset password?\n1. Yes\n2. No')
            reset_pass = int(input())
            # Reset password Function
            if reset_pass==1:
                new_pass = input("Enter your New pass: ")
                if self.role=='elder':
                    sql = "UPDATE elders set password = %s WHERE mobile = %s"
                    val = ( new_pass, self.mobile)
                    mycursor.execute(sql, val)
                    mydb.commit()
                    print("Password Reset Successfully.")
                elif self.role=='younger':
                    sql = "UPDATE youngers set password = %s WHERE mobile = %s"
                    val = ( new_pass, self.mobile)
                    mycursor.execute(sql, val)
                    mydb.commit()
                    print("Password Reset Successfully.")
            else:
                import index    # due to mutual importing we are importing here just before methodcalling
                index.Welcome() 
