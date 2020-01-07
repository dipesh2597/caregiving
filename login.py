import younger_profile
import mysql.connector


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="password",
  use_pure=True,
  database="caregiving"
)

mycursor = mydb.cursor()

class Elder_Login:
    def __init__(self, mobile, password):
        self.mobile = mobile
        self.password = password

    #login Function
    def login(self,mobile,password):
        #retrieving passwords for registered mobile no from both table
        sql = f'SELECT password FROM elders WHERE mobile={mobile}'
        mycursor.execute(sql)
        user_info = mycursor.fetchall() # fetchall provides empty list if record does not exists
        if user_info==[]:
            print(f'{mobile} Not registered. Please try to register first')
            import index      # due to mutual importing we are importing here just before method calling
            index.Welcome()
        sql = f'SELECT password FROM elders WHERE mobile={mobile}'
        mycursor.execute(sql)
        user_info = mycursor.fetchone()
        if password==user_info[0]:
            print("Logged IN")
            import elder_profile
            elder_pro= elder_profile.Elder_Profile(mobile)
            elder_pro.Dashboard_elder()

        else:
            print("Wrong mobile number and password")
            index.Welcome()


class Younger_Login:
    def __init__(self, mobile, password):
        self.mobile = mobile
        self.password = password

        #login Function
    def login(self,mobile,password):
        #retrieving passwords for registered mobile no from both table
        sql = f'SELECT password FROM youngers WHERE mobile={mobile}'
        mycursor.execute(sql)
        user_info = mycursor.fetchall()     # fetchall provides empty list if record does not exists
        if user_info==[]:
            print(f'{mobile} Not registered. Please try to register first')
            import index      # due to mutual importing we are importing here just before method calling
            index.Welcome()
        sql = f'SELECT password FROM youngers WHERE mobile={mobile}'
        mycursor.execute(sql)
        user_info = mycursor.fetchone()
        if password==user_info[0]:
            print("Logged IN")
            younger_pro = younger_profile.Younger_Profile(mobile)
            younger_pro.Dashboard_younger()

        else:
            print("Wrong mobile number and password")
            index.Welcome()
