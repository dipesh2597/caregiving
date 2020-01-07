
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
    def __init__(self, mobile):
        self.mobile = mobile

    def Dashboard_elder(self):
        sql = f'SELECT available FROM elders where mobile = {self.mobile}'
        mycursor.execute(sql)
        user_info = mycursor.fetchone()
        if user_info[0]==1:
            print("You are currently Available to take care of.\n1.Make Unavailable\n2.Fund:\n3.Request\n4.Take Care Name\n5. LogOut")
            choice = int(input())
            if choice==1:
                self.changestatus()
            elif choice==2:
                self.fund()
            elif choice==3:
                self.Request()

        else:
            print("You are currently Unavailable to take care of.\n1.Make Unavailable\n2.Fund:\n3.Request\n4.Take Care Name")
            choice = int(input())
            if choice==1:
                self.changestatus()
            elif choice==2:
                self.fund()
            elif choice==3:
                self.Request()
            elif choice==4:
                self.takeCareName()
            elif choice==5:
                self.logout()

    def fund(self):
        sql = f'SELECT fund FROM elders where mobile = {self.mobile}'
        mycursor.execute(sql)
        user_fund = mycursor.fetchone()
        if user_fund[0]==None:
            print("You didn't allocated any amount yet.")
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
            key = int(input("Press 1 to go to dashboard\n"))
            if key==1:
                self.Dashboard_elder()

    def changestatus(self):
        sql = f'SELECT available FROM elders where mobile = {self.mobile}'
        mycursor.execute(sql)
        user_info = mycursor.fetchone()
        if user_info[0]==1:
            sql = f'UPDATE elders set available = 0 WHERE mobile = {self.mobile}'
            val = (self.mobile)
            mycursor.execute(sql, val)
            mydb.commit()
            self.Dashboard_elder()
        else:
            sql = f'UPDATE elders set available = 1 WHERE mobile = {self.mobile}'
            val = (self.mobile)
            mycursor.execute(sql, val)
            mydb.commit()
            self.Dashboard_elder()
            
    def Request(self):
        sql = f'SELECT PK_elder_id from elders WHERE mobile={self.mobile}'
        val=(self.mobile)
        mycursor.execute(sql, val)
        elder_id = mycursor.fetchone()
        sql = f'SELECT younger_id from request WHERE elder_id={elder_id[0]}'
        val =(elder_id[0])
        mycursor.execute(sql, val)
        younger_id = mycursor.fetchall()
        print("Here is the list of youngers who sent you request to take care of you.\nPLease Enter the request no to accept request or press 0 for rejecting all remaining requests.")
        for i in range(len(younger_id)):
            sql = f'SELECT name from youngers WHERE PK_younger_id={younger_id[i][i]}'
            val = (younger_id[i][i])
            mycursor.execute(sql, val)
            younger_name = mycursor.fetchall()
            print(f'{i+1}. {younger_name[i][i]} sent you a request to take care of you.')
        request_no = int(input())
        for i in range(len(younger_id)):
            sql = f'SELECT name from youngers WHERE PK_younger_id={younger_id[i][i]}'
            val = (younger_id[i][i])
            mycursor.execute(sql, val)
            younger_name = mycursor.fetchall()
            if i==(request_no-1) and request_no!=0:
                sql = "SELECT PK_request_id FROM request where younger_id = %s and elder_id = %s"
                val = (younger_id[i][i], elder_id[0])
                mycursor.execute(sql, val)
                request_id = mycursor.fetchone()
                sql = f'delete from request WHERE PK_request_id= {request_id[0]}'
                val=(request_id[0])
                mycursor.execute(sql,val)
                sql=f'select name from elders where PK_elder_id={elder_id[0]}'
                val=(elder_id[0])
                mycursor.execute(sql, val)
                elder_name = mycursor.fetchone()
                # updationg elder table
                sql = f'UPDATE elders set younger_name = {elder_name[0]} WHERE PK_elder_id = {elder_id[0]}'
                val=(elder_name[0], elder_id[0])
                mycursor.execute(sql, val)
                mydb.commit()
                # updating youngers table
                if len(elder_name)<=4:
                    sql = f'UPDATE youngers set elder_name = {younger_name[0]} WHERE PK_elder_id = {younger_id[i][i]}'
                    val=(younger_name[0], younger_id[i][i])
                    mycursor.execute(sql, val)
                    mydb.commit() 
                else:
                    print("You have already taking care of 4 elders")               
            print(f'{i+1}. Request Accepted for {younger_name[i][i]}')


    def takeCareName(self):
        sql=f'select younger_name from elders where mobile={self.mobile]}'
        val=(self.mobile)
        mycursor.execute(sql, val)
        younger_name = mycursor.fetchone()
        print(f'{younger_name[0] is doing you take care stuff.}')

    def logout(self):
        import index
        index.Welcome()