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
    def __init__(self,mobile):
        self.mobile = mobile

    def Dashboard_younger(self):
        sql = f'SELECT elders_name FROM youngers where mobile = {self.mobile}'
        mycursor.execute(sql)
        elders_list = mycursor.fetchone()
        if elders_list[0]==None:
            a=0
        else:
            a = len(elders_list)
        
        print(f'Currentlty you are taking care of {a} Elders\nYou can request for {4-a} more elders to take care of.\n1. View list of Available elders to take care of.\n2. LogOut')
        younger_choice = int(input())
        if younger_choice==1:
            self.elder_list()

        elif younger_choice==2:
            self.logout()


    def elder_list(self, user=None):
        sql = f'SELECT name, mobile, fund FROM elders WHERE available=True'
        mycursor.execute(sql)
        elders_list = mycursor.fetchall()
        j=1
        for num in elders_list:
            if j==user:
                pass 
            elif user==0:
                self.Dashboard_younger()
                break
            else:
                print(f'\n{j}.', end=' ')
            for i in num:
                if j==user:
                    pass 
                else:
                    print(f'{i}',end='\n   ')
            j+=1
        
        self.Request_elder()

    def Request_elder(self):
        user=int(input("Please Select the user whome you want to reqeust to take care of.\n"))
        sql = f'SELECT name, mobile, fund FROM elders WHERE available=True'
        mycursor.execute(sql)
        elders_list = mycursor.fetchall()
        elder_mob=elders_list[user-1][1]
        sql = f'SELECT PK_younger_id FROM youngers WHERE mobile={self.mobile}'
        val = (self.mobile)
        mycursor.execute(sql)
        younger_id = mycursor.fetchone()
        sql = f'SELECT PK_elder_id FROM elders WHERE mobile={elder_mob}'
        val = (elder_mob)
        mycursor.execute(sql)
        elder_id = mycursor.fetchone()
        sql = "INSERT INTO request (younger_id, elder_id) VALUES (%s, %s)"
        val = (younger_id[0], elder_id[0])
        mycursor.execute(sql, val)
        mydb.commit()
        print(f'Request sent!')
        self.elder_list(user)

    def logout(self):
        import index
        index.Welcome()