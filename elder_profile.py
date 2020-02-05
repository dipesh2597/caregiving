import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="password",
  use_pure=True,
  database="caregiving"
)

mycursor = mydb.cursor()

class Elder_Profile:
    def __init__(self, mobile, password):
        self.mobile = mobile
        self.password = password
        sql = f'SELECT name, PK_elder_id from elders WHERE mobile={self.mobile}'
        val=(self.mobile)
        mycursor.execute(sql, val)
        elder_details = mycursor.fetchone()
        self.elderName = elder_details[0]
        self.elderID = elder_details[1]

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
            self.dashboardElder()

        else:
            print("Wrong mobile number and password")
            index.Welcome()

    def dashboardElder(self):
        sql = f'SELECT available FROM elders where mobile = {self.mobile}'
        mycursor.execute(sql)
        user_info = mycursor.fetchone()
        if user_info[0]==1:
            print("You are currently Available to take care of.\n1.Make Unavailable\n2.Fund\n3.Request\n4.Take Care Name\n5.Give review and rating for a younger\n6.LogOut")
            choice = int(input())
            if choice==1:
                self.changeStatus()
                self.dashboardElder()
            elif choice==2:
                self.allocateFund()
            elif choice==3:
                self.showRequest()
            elif choice==4:
                self.takeCareName()
            elif choice==5:
                self.review()
            elif choice==6:
                self.logOut()

        else:
            print("You are currently Unavailable to take care of.\n1.Make Available\n2.Log Out")
            choice = int(input())
            if choice==1:
                self.changeStatus()
                self.dashboardElder()
            elif choice==2:
                self.logOut()

    def allocateFund(self):
        sql = f'SELECT fund FROM elders where mobile = {self.mobile}'
        mycursor.execute(sql)
        user_fund = mycursor.fetchone()
        if user_fund[0]==None:
            print("You didn't allocated any amount yet.")
            changefund = int(input("1.Allocated fund.\n2.Cancel\n"))
        else:
            print(f'your current allocated fund is {user_fund[0]}')
            changefund = int(input("1.Change allocated fund.\n2.Cancel\n"))
        if changefund==1:
            newFund=input("Enter new amount to allocate\n")
            sql1 = "UPDATE elders set fund = %s WHERE mobile = %s"
            val1 = (newFund, self.mobile)
            mycursor.execute(sql1, val1)
            mydb.commit()
            print(f'Your new allocated fun is {newFund}')
        
        self.dashboardElder()

    def changeStatus(self):
        sql = f'SELECT available FROM elders where mobile = {self.mobile}'
        mycursor.execute(sql)
        user_info = mycursor.fetchone()
        if user_info[0]==1:
            sql = f'UPDATE elders set available = 0 WHERE mobile = {self.mobile}'
            val = (self.mobile)
            mycursor.execute(sql, val)
            mydb.commit()
        else:
            sql = f'UPDATE elders set available = 1 WHERE mobile = {self.mobile}'
            val = (self.mobile)
            mycursor.execute(sql, val)
            sql = f'UPDATE elders set FK_younger_id = null WHERE PK_elder_id = {self.elderID}'
            val = (self.elderID)
            mycursor.execute(sql, val) 
            mydb.commit()
            
    def showRequest(self):
        # younger's details who is currently taking care of logged in user
        sql = f'SELECT FK_younger_id from elders WHERE PK_elder_id = {self.elderID}'
        val = (self.elderID)
        mycursor.execute(sql, val)
        eldersYounger= mycursor.fetchone()
        eldersYoungerID = eldersYounger[0]
        if eldersYoungerID is not None:
            print("Someone is already taking care of you. So no one can send you request.")
            self.dashboardElder()
        else:
            sql = f'SELECT FK_younger_id from request WHERE FK_elder_id={self.elderID}'
            val =(self.elderID)
            mycursor.execute(sql, val)
            younger_id = mycursor.fetchall()
            if len(younger_id)==0:
                input("Currently no one requested you. Press any key to go to your Dashboard.\n")
                self.dashboardElder()
            else:
                # printing list to younger how has sent a request
                print("Here is the list of youngers who sent you request to take care of you.\nPlease Enter the request no to accept request.")
                for i in range(len(younger_id)):
                    sql = f'SELECT name from youngers WHERE PK_younger_id={younger_id[i][0]}'
                    val = (younger_id[i][0])
                    mycursor.execute(sql, val)
                    younger_name = mycursor.fetchall()
                    print(f'{i+1}. {younger_name[0][0]} sent you a request to take care of you.')
                request_no = int(input())
                sql = f'UPDATE elders set FK_younger_id = {younger_id[request_no-1][0]} WHERE PK_elder_id = {self.elderID}'
                val = (self.elderID)
                mycursor.execute(sql, val)
                self.changeStatus()
                sql = f'DELETE FROM request WHERE FK_elder_id = {self.elderID}'
                val = (self.elderID)
                mycursor.execute(sql, val)
                mydb.commit()     
                print('Request Accepted')
                self.dashboardElder()

    def takeCareName(self):
        sql = f'SELECT FK_younger_id from elders WHERE PK_elder_id = {self.elderID}'
        val = (self.elderID)
        mycursor.execute(sql, val)
        eldersYounger= mycursor.fetchone()
        eldersYoungerID = eldersYounger[0]
        if eldersYoungerID is None:
            print("No one is taking care of you. If your Unavailable then make yourself available for taking care of.")
            self.dashboardElder()
        else:
            sql = f'SELECT name from elders WHERE PK_elder_id = {eldersYoungerID}'
            val = (eldersYoungerID)
            mycursor.execute(sql, val)
            eldersYounger= mycursor.fetchone()
            eldersYoungerNAME = eldersYounger[0]
            print(f'{eldersYoungerNAME} is taking care of you currently.')

    def review(self):
        youngerNumber = int(input("Please enter mobile number of younger for whome you want to give review and rating.\n"))
        review = input("Please write your review.\n")
        rating = int(input("please give rating out of 10.\n"))
        sql = "UPDATE youngers set review = %s, rating = %s WHERE mobile = %s"
        val = (review, rating, youngerNumber)
        mycursor.execute(sql, val)
        mydb.commit()
        print("Review rating updated successfully\n")
        self.dashboardElder()

    def logOut(self):
        import index
        index.Welcome()