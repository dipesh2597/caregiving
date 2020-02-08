from db import *

class YoungerProfile():
    def __init__(self, email, password):
        self.email = email
        self.password = password
        sql = f'SELECT PK_user_id, name FROM users WHERE email = "{self.email}" '
        mycursor.execute(sql)
        user_id = mycursor.fetchone()
        self.user_id = user_id[0]
        self.younger_name = user_id[1]
        sql = f'SELECT PK_younger_id FROM youngers WHERE FK_user_id={self.user_id}'
        mycursor.execute(sql)
        younger_id = mycursor.fetchone()
        self.younger_id=younger_id[0]
        sql = f'SELECT FK_younger_id from elders where FK_younger_id = {self.younger_id}'
        mycursor.execute(sql)
        self.youngerCount = mycursor.fetchall()

    def sign_up(self, user_id):
        sql = "INSERT INTO youngers (FK_user_ID) VALUES (%s)"
        val = (user_id)
        mycursor.execute(sql, val)
        print("inserted")
        mydb.commit()

    def log_in(self):
        #retrieving passwords for registered mobile no from both table
        sql = f'SELECT password FROM users WHERE email= "{self.email}" '
        mycursor.execute(sql)
        user_info = mycursor.fetchone()     # fetchall provides empty list if record does not exists
        if user_info==[]:
            print(f'{self.email} ot registered. Please try to register first')
            import index      # due to mutual importing we are importing here just before method calling
        elif self.password==user_info[0]:
            print("Logged IN")
            self.dashboard_younger()
        else:
            print("Wrong email and password")
            import index

    def dashboard_younger(self):
        elderCount = len(self.youngerCount)
        print(f'Currentlty you are taking care of {elderCount} Elders\nYou can request for {4-elderCount} more elders to take care of.\n1.View list of Available elders to take care of.\n2.Give review and rating for a elder\n3.LogOut')
        choice = int(input())
        if choice==1:
            self.request_elder()
        elif choice==2:
            self.review()
        elif choice==3:
            self.log_out()

    def request_elder(self):
        if len(self.youngerCount)>=4:
            print("You are already taking care of 4 peopele. Now you can not request for anyone else.")
            self.dashboard_younger()
        #if current younger requested a elder earlier then we need not to display that elder again
        else:
            sql = f'SELECT FK_user_id, PK_elder_id FROM elders WHERE available=True and PK_elder_id not in (SELECT FK_elder_id from request WHERE FK_younger_id={self.younger_id})'
            mycursor.execute(sql)
            elders_user_id = mycursor.fetchall()
            print(elders_user_id)
            j=1
            for num in elders_user_id:
                print(f'\n{j}.', end=' ')
                sql = f'SELECT name from users WHERE PK_user_id = {num[0]}'
                mycursor.execute(sql)
                name=mycursor.fetchone()
                print(name[0])
                j+=1
            print()
        user=int(input("Please Select the user whome you want to reqeust to take care of.\nEnter 0 to go to dashboard\n"))  
        elder_id = elders_user_id[user-1][1]
        sql = "INSERT INTO request (FK_younger_id, FK_elder_id) VALUES (%s, %s)"
        val = (self.user_id, elder_id)
        mycursor.execute(sql, val)
        mydb.commit()
        if user==0:
            self.dashboard_younger()
        else:
            print(f'Request sent!')
            n = int(input("1.Dashboard\n2.Send another request\n"))
            if n==1:
                self.dashboard_younger()
            elif n==2:
                self.request_elder()

    def review(self):
        elder_number=100
        elder_number = int(input("Please enter mobile number of elder for whome you want to give review and rating.\n"))
        sql = f'select PK_user_id from users where mobile = {elder_number} '
        val=(elder_number)
        mycursor.execute(sql,val)
        user_id = mycursor.fetchone()
        review = input("Please write your review.\n")
        rating = int(input("please give rating out of 10.\n"))
        sql = "Insert into reviews (FK_user_id, review, rating, review_by) VALUES (%s, %s, %s, %s)"
        val = (user_id[0], review, rating, self.younger_name)
        mycursor.execute(sql, val)
        sql = f'SELECT rating from reviews WHERE FK_user_id = {user_id[0]}'
        mycursor.execute(sql)
        ratings=mycursor.fetchall()
        avg_rating=0
        for i in ratings:
            avg_rating+=i[0]
        avg_rating/=len(ratings)
        sql = f'UPDATE elders set rating ={avg_rating} WHERE FK_user_id = {user_id[0]}'
        mycursor.execute(sql)
        mydb.commit()
        print("Review rating updated successfully\n")
        self.dashboard_younger()

    def log_out(self):
        import index