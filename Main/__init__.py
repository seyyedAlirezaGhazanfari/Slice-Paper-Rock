import mysql.connector
#print('welcome to connection to database')
mydb = mysql.connector.connect(host="localhost",
                               username="root",
                               password = "Alireza33179217",
                               database = "game"
                               )
mycursor = mydb.cursor()
sql =""
val=""
print('database is ready')

class Player:
    listOfPlayers = []
    def __init__(self,username, password):
        self.username = username
        self.password = password
        Player.listOfPlayers.append(self)
    @staticmethod
    def is_there_player_by(username1):
        sql = "SELECT * FROM players where username = %s "
        val = (username1,)
        mycursor.execute(sql,val)
        newcursor = mycursor.fetchall()
        if len(newcursor)==0:
            return False
        else:
            return True

    @staticmethod
    def find_player(username,password):
        for player in Player.listOfPlayers:
            if Player(player).username == username and Player(player).password == password:
                return player
def enter_to_game_page(username,password):
    sql = "select username from players where logged='True'"
    mycursor.execute(sql)
    new_result = mycursor.fetchall()
    for x in new_result:
        print(x[0])
    while True:
        enemy_username = input('enter your enemy username : ')
        if enemy_username == 'back':
            break
        is_this_invalid = True
        for x in new_result:
            if x[0]==enemy_username:
                is_this_invalid = False
                break
        if is_this_invalid:
            print('invalid name')
            continue
        else:
            print('here is your enemy')
            command_of_gamer1 = input('enter s,r,p  :     ')
            command_of_gamer2 = input('enter s,r,p  :     ')
            sql = "insert into games (player1_id,player2_id) values (%s,%s)"
            val = (username,enemy_username)
            mycursor.execute(sql,val)
            mydb.commit()
            if ((command_of_gamer1=='s' and command_of_gamer2=='p') or (command_of_gamer1 =='r' and command_of_gamer2 == 's' ) or (command_of_gamer1 == 'p' and command_of_gamer2=='r')):
                print('gamer 1 won')
                sql = "Select point from players where username = %s "
                val = (username,)
                mycursor.execute(sql,val)
                result = mycursor.fetchone()
                sql = "UPDATE players set point = %s where username = %s"
                val = (result[0]+1,username)
                mycursor.execute(sql,val)
                mydb.commit()
            elif  ((command_of_gamer2=='s' and command_of_gamer1=='p') or (command_of_gamer2 =='r' and command_of_gamer1 == 's') or (command_of_gamer2 == 'p' and command_of_gamer1=='r') )  :
                print('gamer 2 won')
                sql = "Select point from players where username = %s "
                val = (enemy_username,)
                mycursor.execute(sql, val)
                result = mycursor.fetchone()
                sql = "UPDATE players set point = %s where username = %s"
                val = (result[0] + 1,enemy_username)
                mycursor.execute(sql, val)
                mydb.commit()
            elif ((command_of_gamer2==command_of_gamer1)):
                print('no one won')
            else:
                print('invalid input')



def logout(username):
    sql = "update players set logged = 'False' where username = %s"
    val = (username,)
    mycursor.execute(sql,val)
    mydb.commit()
    print('logout successfully')

def login():
    print('welcome to login page:\n')
    username = input("enter username : ")
    password = input("enter password : ")
    #sql = 'SELECT logged from players where username = %s and password = %s'
    val = (username,password)
    sql1 = "Select logged From players where username = %s and password = %s"
    mycursor.execute(sql1,val)
    confirm = mycursor.fetchone()
    if confirm == None:
        print('hey null user')
        return -1
    elif confirm[0]=='True' :
        print('hey you are wrong')
        return 0
    sql = 'UPDATE players set logged = "True" where (username = %s and password = %s and logged = "False")'
    mycursor.execute(sql,val)
    mydb.commit()
    print('login completed')
    command = input('enter a command : ')
    if command=='1':
        print('welcome back to main page')
        return
    elif command == '2' :
        print('logout')
        logout(username)
        return
    elif command == '3':
        print('welcome to game')
        enter_to_game_page(username,password)


def show_table_of_point():
    print('table is this until now:\n')
    sql = 'SELECT username, point From players order by username desc '
    mycursor.execute(sql)
    myList = mycursor.fetchall()
    for x in myList:
        print(x)
def register():
    print('welcome to registering page')
    username = input('enter username    :   ')
    password = input('enter password    :   ')
    if not Player.is_there_player_by(username):
        sql = "INSERT INTO players (username,password,point,logged) VALUES (%s,%s,0, 'False')"
        val = (username,password)
        mycursor.execute(sql,val)
        mydb.commit()
        print('you are registered')

    else:
        print('hey this is problem')



def run():
    print('hello welcome to this game')
    while True:
        command = input('enter your command 1)register\n2)login\n3)table\n4)exit\n5)logout  :')
        if command=='1':
            print('register')
            register()
        elif command=='2':
            print('login')
            login()
        elif command=='3':
            print('table of points')
            show_table_of_point()
            print("\n")
        elif command == '4':
            print('exit')
            break
        elif command == '5':
            print('logout')
            username = input('enter your username  :   ')
            logout(username)
        else:
            print('error')
run()