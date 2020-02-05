import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="password",
  use_pure=True,
  database="caregiving"
)

mycursor = mydb.cursor()

class Younger_Profile:
    def __init__(self, mobile, password):
        self.mobile = mobile
        self.password = password
        sql = f'SELECT PK_younger_id FROM youngers WHERE mobile={self.mobile}'
        mycursor.execute(sql)
        younger_id = mycursor.fetchone()
        self.youngerID=younger_id[0]
        sql = f'SELECT FK_younger_ID from elders where FK_younger_ID = {self.youngerID}'
        mycursor.execute(sql)
        self.youngerCount = mycursor.fetchall()

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
            self.dashboardYounger()

        else:
            print("Wrong mobile number and password")
            index.Welcome()

    def dashboardYounger(self):
        elderCount = len(self.youngerCount)
        print(f'Currentlty you are taking care of {elderCount} Elders\nYou can request for {4-elderCount} more elders to take care of.\n1. View list of Available elders to take care of.\n3.Give review and rating for a elder\n2. LogOut')
        choice = int(input())
        if choice==1:
            self.elder_list()
        elif choice==2:
            self.review()
        elif choice==3:
            self.logOut()


    def elder_list(self):
        if len(self.youngerCount)>=4:
            print("You are already taking care of 4 peopele. Now you can not request for anyone else.")
            self.dashboardYounger()
        #if current younger requested a elder earlier then we need not to display that elder again
        else:
            sql = f'SELECT name, mobile, fund FROM elders WHERE available=True and PK_elder_id not in (SELECT   FK_elder_id from request WHERE FK_younger_id={self.youngerID})'
            mycursor.execute(sql)
            elders_list = mycursor.fetchall()
            j=1
            for num in elders_list:
                print(f'\n{j}.', end=' ')
                for i in num:
                    print(f'{i}',end='\n   ')
                j+=1
            print()
            self.requestElder()

    def requestElder(self):
        user=int(input("Please Select the user whome you want to reqeust to take care of.\nEnter 0 to go to dashboard\n"))
        sql = f'SELECT name, mobile, fund FROM elders WHERE available=True'
        mycursor.execute(sql)
        elders_list = mycursor.fetchall()
        elder_mob=elders_list[user-1][1]
        sql = f'SELECT PK_elder_id FROM elders WHERE mobile={elder_mob}'
        val = (elder_mob)
        mycursor.execute(sql)
        elder_id = mycursor.fetchone()
        sql = "INSERT INTO request (FK_younger_id, FK_elder_id) VALUES (%s, %s)"
        val = (self.youngerID, elder_id[0])
        mycursor.execute(sql, val)
        mydb.commit()
        if user==0:
            self.dashboardYounger()
        else:
            print(f'Request sent!')
            n = int(input("1.Dashboard\n2.Send another request\n"))
            if n==1:
                self.dashboardYounger()
            elif n==2:
                self.elder_list()

    def review(self):
       elderNumber = int(input("Please enter mobile number of elder for whome you want to give review andrating.\n"))
       review = input("Please write your review.\n")
       rating = int(input("please give rating out of 10.\n"))
       sql = "UPDATE elders set review = %s, rating = %s WHERE mobile = %s"
       val = (review, rating, elderNumber)
       mycursor.execute(sql, val)
       mydb.commit()
       print("Review rating updated successfully\n")
       self.dashboardYounger()

    def logOut(self):
        import index
        index.Welcome()
