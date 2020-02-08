from db import *

class ElderProfile():
    def __init__(self, email, password):
        self.email = email
        self.password = password
        sql = f'SELECT PK_user_id, name FROM users WHERE email = "{self.email}" '
        mycursor.execute(sql)
        user_id = mycursor.fetchone()
        self.user_id = user_id[0]
        self.elder_name = user_id[1]
        sql = f'SELECT PK_elder_id FROM elders WHERE FK_user_id={self.user_id}'
        mycursor.execute(sql)
        elder_id = mycursor.fetchone()
        self.elder_id=elder_id[0]

    def sign_up(self, user_id):
        sql = "INSERT INTO elders (FK_user_ID) VALUES (%s)"
        val = (self.user_id)
        mycursor.execute(sql, val)
        mydb.commit()

    def log_in(self):
        #retrieving passwords for registered mobile no from both table
        sql = f'SELECT password FROM users WHERE email= "{self.email}" '
        mycursor.execute(sql)
        user_info = mycursor.fetchone()     # fetchall provides empty list if record does not exists
        if user_info==[]:
            print(f'{self.email} not registered. Please try to register first')
            import index      # due to mutual importing we are importing here just before method calling
        elif self.password==user_info[0]:
            print("Logged IN")
            self.dashboard_elder()
        else:
            print("Wrong email and password")
            import index

    def dashboard_elder(self):
        sql = f'SELECT available FROM elders where PK_elder_id = {self.elder_id}'
        mycursor.execute(sql)
        user_info = mycursor.fetchone()
        if user_info[0]==1:
            print("You are currently Available to take care of.\n1.Make Unavailable\n2.Fund\n3.Request\n4.Take Care Name\n5.Give review and rating for a younger\n6.LogOut")
            choice = int(input())
            if choice==1:
                self.change_status()
                self.dashboard_elder()
            elif choice==2:
                self.allocate_fund()
            elif choice==3:
                self.show_request()
            elif choice==4:
                self.take_care_name()
            elif choice==5:
                self.review()
            elif choice==6:
                self.log_out()

        else:
            print("You are currently Unavailable to take care of.\n1.Make Available\n2.Log Out")
            choice = int(input())
            if choice==1:
                self.change_status()
                self.dashboard_elder()
            elif choice==2:
                self.log_out()

    def allocate_fund(self):
        sql = f'SELECT fund FROM elders where PK_elder_id = {self.elder_id}'
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
            sql1 = "UPDATE elders set fund = %s WHERE Pk_elder_id = %s"
            val1 = (newFund, self.elder_id)
            mycursor.execute(sql1, val1)
            mydb.commit()
            print(f'Your new allocated fun is {newFund}')
        
        self.dashboard_elder()

    def change_status(self):
        sql = f'SELECT available FROM elders where PK_elder_id = {self.elder_id}'
        mycursor.execute(sql)
        user_info = mycursor.fetchone()
        if user_info[0]==1:
            sql = f'UPDATE elders set available = 0 WHERE PK_elder_id = {self.elder_id}'
            val = (self.elder_id)
            mycursor.execute(sql, val)
            mydb.commit()
        else:
            sql = f'UPDATE elders set available = 1 WHERE PK_elder_id = {self.elder_id}'
            val = (self.elder_id)
            mycursor.execute(sql, val)
            sql = f'UPDATE elders set FK_younger_id = null WHERE PK_elder_id = {self.elder_id}'
            val = (self.elder_id)
            mycursor.execute(sql, val) 
            mydb.commit()
            
    def show_request(self):
        # younger's details who is currently taking care of logged in user
        sql = f'SELECT FK_younger_id from elders WHERE PK_elder_id = {self.elder_id}'
        val = (self.elder_id)
        mycursor.execute(sql, val)
        elders_younger= mycursor.fetchone()
        elders_younger_id = elders_younger[0]
        if elders_younger_id is not None:
            print("Someone is already taking care of you. So no one can send you request.")
            self.dashboard_elder()
        else:
            sql = f'SELECT FK_younger_id from request WHERE FK_elder_id={self.elder_id}'
            val =(self.elder_id)
            mycursor.execute(sql, val)
            younger_id = mycursor.fetchall()
            if len(younger_id)==0:
                input("Currently no one requested you. Press any key to go to your Dashboard.\n")
                self.dashboard_elder()
            else:
                # printing list to younger how has sent a request
                print("Here is the list of youngers who sent you request to take care of you.\nPlease Enter the request no to accept request.")
                for i in range(len(younger_id)):
                    sql = f'SELECT name from users WHERE PK_user_id={younger_id[i][0]}'
                    val = (younger_id[i][0])
                    mycursor.execute(sql, val)
                    younger_name = mycursor.fetchone()

                    print(f'{i+1}. {younger_name[0]} sent you a request to take care of you.')

                request_no = int(input())
                sql = f'UPDATE elders set FK_younger_id = {younger_id[request_no-1][0]} WHERE PK_elder_id = {self.elder_id}'
                val = (self.elder_id)
                mycursor.execute(sql, val)
                self.change_status()
                sql = f'DELETE FROM request WHERE FK_elder_id = {self.elder_id}'
                val = (self.elder_id)
                mycursor.execute(sql, val)
                mydb.commit()     
                print('Request Accepted')
                self.dashboard_elder()

    def take_care_name(self):
        sql = f'SELECT FK_younger_id from elders WHERE PK_elder_id = {self.elder_id}'
        val = (self.elder_id)
        mycursor.execute(sql, val)
        elders_younger= mycursor.fetchone()
        elders_younger_id = elders_younger[0]
        if elders_younger_id is None:
            print("No one is taking care of you. If your Unavailable then make yourself available for taking care of.")
            self.dashboard_elder()
        else:
            sql = f'SELECT name from users WHERE PK_user_id = {elders_younger_id}'
            val = (elders_younger_id)
            mycursor.execute(sql, val)
            elders_younger= mycursor.fetchone()
            elders_younger_name = elders_younger[0]
            print(f'{elders_younger_name} is taking care of you currently.')

    def review(self):
        younger_number = int(input("Please enter mobile number of elder for whome you want to give review and rating.\n"))
        sql = f'select PK_user_id from users where mobile = {younger_number} '
        val=(younger_number)
        mycursor.execute(sql,val)
        user_id = mycursor.fetchone()
        review = input("Please write your review.\n")
        rating = int(input("please give rating out of 10.\n"))
        sql = "Insert into reviews (FK_user_id, review, rating, review_by) VALUES (%s, %s, %s, %s)"
        val = (user_id[0], review, rating, self.elder_name)
        mycursor.execute(sql, val)
        sql = f'SELECT rating from reviews WHERE FK_user_id = {user_id[0]}'
        mycursor.execute(sql)
        ratings=mycursor.fetchall()
        avg_rating=0
        for i in ratings:
            avg_rating+=i[0]
        avg_rating/=len(ratings)
        sql = f'UPDATE youngers set rating ={avg_rating} WHERE FK_user_id = {user_id[0]}'
        mycursor.execute(sql)
        mydb.commit()
        print("Review rating updated successfully\n")
        self.dashboard_elder()

    def log_out(self):
        import index
