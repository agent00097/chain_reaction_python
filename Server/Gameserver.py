import pickle, re, time, ssl
#import sys, random
from socket import AF_INET, SOCK_STREAM, timeout, error, socket
import hashlib, os, binascii
from threading import Thread, Lock
import mysql.connector



mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="gameserver"
)

mycursor = mydb.cursor()
ports = 60000
namereg = re.compile("^[a-zA-Z0-9]{0,20}$")
regpass = re.compile("^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$")
LOCALHOST = "127.0.0.1"
server_port = 49999
buffer = []
connbuffer = {}
userlist = {}
occupied_ports = []
gamerooms = []
lock_buf = Lock()
# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 40
HEIGHT = 40
# This sets the margin between each cell
MARGIN = 5
#defining turn
#turn = 1

done = False

def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 10)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac(
        'sha512', provided_password.encode('utf-8'), salt.encode('ascii'), 10)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

def client_specific_server(portn, clientname, recon_flag):
    lhost = "127.0.0.1"
    port = portn
    print(clientname)
    try:
        serversock = socket(AF_INET, SOCK_STREAM)
        serversock.bind((lhost, port))
        serversock.listen(1)
    except:
        return
    #while True:
    try:
        connect, clientadd = serversock.accept()
    except:
        connect.close()
        return
    try:
        connssl = ssl.wrap_socket(connect, server_side=True, certfile="server.crt", keyfile="server.key")
        connssl.settimeout(300)
    except:
        connssl.close()
        return
    try:
        inputd = connssl.recv(1024)
    except:
        connssl.close()
        return
    #data = pickle.loads(inputd)
    try:
        mycursor.execute("SELECT * FROM user WHERE name = %s;", (clientname,))
        x = mycursor.fetchone()
        a = []
        a.append(x[2])
        a.append(x[3])
        a.append(x[4])
        mycursor.execute("SELECT * FROM games WHERE player1=%s OR player2=%s;", (clientname, clientname,))
        myresult = mycursor.fetchall()
        for x in myresult:
            a.append(x[3])
        sentence = pickle.dumps(a)
    except:
        connssl.close()
        return
    try:    
        connssl.send(sentence)
    except:
        connssl.close()
        return
    if recon_flag == 1:
        sentence = pickle.dumps("You are added in Buffer")
    else:
        sentence = pickle.dumps("Reconnecting to your game")

    try:
        connssl.send(sentence)
    except:
        connssl.close()
        return

    lock_buf.acquire()
    #userlist[clientname].append(serversock)
    if recon_flag == 1:
        buffer.append(clientname)
    connbuffer[clientname] = connssl
    lock_buf.release()
    return
    #connbuffer[clientname].close()


def room_creator():
    while True:
        time.sleep(5)
        lock_buf.acquire()
        n = len(buffer)
        if n < 2:
            lock_buf.release()
            for c in buffer:
                data = pickle.dumps("Waiting for another user")
                try:
                    connbuffer[c].send(data)
                except:
                    print(str(c)+" is down.")
        elif n == 0:
            lock_buf.release()

        else:
            for i in range(0, n, 2):
                if i+1 != n:
                    #rmo=Thread(target=player_game_room, args=(buffer[i],buffer[i+1],))
                    rmo = player_game_room(buffer[i], buffer[i+1])
                    print("Thread is running "+str(i)+" "+str(i+1)+" "+str(n))
                    rmo.start()
            if n%2 == 1:
                last = buffer[n-1]
                print("n2=1")
                buffer.clear
                del buffer[:]
                buffer.append(last)
            else:
                buffer.clear
                del buffer[:]
                print("n2=1")

            lock_buf.release()


class player_game_room(Thread):
    def __init__(self, play1, play2):
        Thread.__init__(self)
        self.play1 = play1
        self.play2 = play2
        self.playerOneAtoms = []
        self.playerTwoAtoms = []
        self.playerOneMoves = []
        self.playerTwoMoves = []
        self.grid = [[0]*10]*10
        self.grid = [([0] * 10) for row in range(10)]
        self.win_check = 0

    def deleteTheAtom(self, row, column):
        if (row, column) in self.playerOneAtoms:
            self.playerOneAtoms.remove(tuple([row, column]))
        if (row, column) in self.playerTwoAtoms:
            self.playerTwoAtoms.remove(tuple([row, column]))


    def checkForRowAndColumn(self, row, column, player_turn):
        if (row == 0 and column == 0):
            #We have to burst at two
            if self.grid[row][column] == 2:
                self.grid[row][column] = 0
                self.deleteTheAtom(row, column)
                self.grid[row+1][column] += 1
                self.deleteTheAtom(row+1, column)
                if player_turn == 1:
                    self.playerOneAtoms.append(tuple([row+1, column]))
                elif player_turn == 2:
                    self.playerTwoAtoms.append(tuple([row+1, column]))
                self.checkForRowAndColumn(row+1, column, player_turn)
                self.grid[row][column+1] += 1
                self.deleteTheAtom(row, column+1)
                if player_turn == 1:
                    self.playerOneAtoms.append(tuple([row, column+1]))
                elif player_turn == 2:
                    self.playerTwoAtoms.append(tuple([row, column+1]))
                self.checkForRowAndColumn(row, column+1, player_turn)

        if (row == 8 and column == 0):
            #We have to burst at two
            if self.grid[row][column] == 2:
                self.grid[row][column] = 0
                self.deleteTheAtom(row, column)
                self.grid[row-1][column] += 1
                self.deleteTheAtom(row-1, column)
                if player_turn == 1:
                    self.playerOneAtoms.append(tuple([row-1, column]))
                elif player_turn == 2:
                    self.playerTwoAtoms.append(tuple([row-1, column]))
                self.checkForRowAndColumn(row-1, column, player_turn)
                self.grid[row][column+1] += 1
                self.deleteTheAtom(row, column+1)
                if player_turn == 1:
                    self.playerOneAtoms.append(tuple([row, column+1]))
                elif player_turn == 2:
                    self.playerTwoAtoms.append(tuple([row+1, column+1]))
                self.checkForRowAndColumn(row, column+1, player_turn)

        if (row == 0 and column == 8):
            if self.grid[row][column] == 2:
                self.grid[row][column] = 0
                self.deleteTheAtom(row, column)
                self.grid[row+1][column] += 1
                self.deleteTheAtom(row+1, column)
                if player_turn == 1:
                    self.playerOneAtoms.append(tuple([row+1, column]))
                elif player_turn == 2:
                    self.playerTwoAtoms.append(tuple([row+1, column]))
                self.checkForRowAndColumn(row+1, column, player_turn)
                self.grid[row][column-1] += 1
                self.deleteTheAtom(row, column-1)
                if player_turn == 1:
                    self.playerOneAtoms.append(tuple([row, column-1]))
                elif player_turn == 2:
                    self.playerTwoAtoms.append(tuple([row+1, column-1]))
                self.checkForRowAndColumn(row, column-1, player_turn)


        if (row == 8 and column == 8):
            if self.grid[row][column] == 2:
                self.grid[row][column] = 0
                self.deleteTheAtom(row, column)
                self.grid[row-1][column] += 1
                self.deleteTheAtom(row-1, column)
                if player_turn == 1:
                    self.playerOneAtoms.append(tuple([row-1, column]))
                elif player_turn == 2:
                    self.playerTwoAtoms.append(tuple([row-1, column]))
                self.checkForRowAndColumn(row-1, column, player_turn)
                self.grid[row][column-1] += 1
                self.deleteTheAtom(row, column-1)
                if player_turn == 1:
                    self.playerOneAtoms.append(tuple([row, column-1]))
                elif player_turn == 2:
                    self.playerTwoAtoms.append(tuple([row, column-1]))
                self.checkForRowAndColumn(row, column-1, player_turn)

        if (row == 0 and column >= 1 and column <= 7):
            #We now check for three
            if self.grid[row][column] == 3:
                self.grid[row][column] = 0
                self.deleteTheAtom(row, column)
                self.grid[row+1][column] += 1
                self.deleteTheAtom(row+1, column)
                if player_turn == 1:
                    self.playerOneAtoms.append(tuple([row+1, column]))
                elif player_turn == 2:
                    self.playerTwoAtoms.append(tuple([row+1, column]))
                self.checkForRowAndColumn(row+1, column, player_turn)
                self.grid[row][column+1] += 1
                self.deleteTheAtom(row, column+1)
                if player_turn == 1:
                    self.playerOneAtoms.append(tuple([row, column+1]))
                elif player_turn == 2:
                    self.playerTwoAtoms.append(tuple([row, column+1]))
                self.checkForRowAndColumn(row, column+1, player_turn)
                self.grid[row][column-1] += 1
                self.deleteTheAtom(row, column-1)
                if player_turn == 1:
                    self.playerOneAtoms.append(tuple([row, column-1]))
                elif player_turn == 2:
                    self.playerTwoAtoms.append(tuple([row, column-1]))
                self.checkForRowAndColumn(row, column-1, player_turn)

        if (row == 8 and column >= 1 and column <= 7):
            if self.grid[row][column] == 3:
                self.grid[row][column] = 0
                self.deleteTheAtom(row, column)
                self.grid[row-1][column] += 1
                self.deleteTheAtom(row-1, column)
                if player_turn == 1:
                    self.playerOneAtoms.append(tuple([row-1, column]))
                elif player_turn == 2:
                    self.playerTwoAtoms.append(tuple([row-1, column]))
                self.checkForRowAndColumn(row-1, column, player_turn)
                self.grid[row][column+1] += 1
                self.deleteTheAtom(row, column+1)
                if player_turn == 1:
                    self.playerOneAtoms.append(tuple([row, column+1]))
                elif player_turn == 2:
                    self.playerTwoAtoms.append(tuple([row, column+1]))
                self.checkForRowAndColumn(row, column+1, player_turn)
                self.grid[row][column-1] += 1
                self.deleteTheAtom(row, column-1)
                if player_turn == 1:
                    self.playerOneAtoms.append(tuple([row, column-1]))
                elif player_turn == 2:
                    self.playerTwoAtoms.append(tuple([row, column-1]))
                self.checkForRowAndColumn(row, column-1, player_turn)

        if (column == 8 and row >= 1 and row <= 7):
            if self.grid[row][column] == 3:
                self.grid[row][column] = 0
                self.deleteTheAtom(row, column)
                self.grid[row-1][column] += 1
                self.deleteTheAtom(row-1, column)
                if player_turn == 1:
                    self.playerOneAtoms.append(tuple([row-1, column]))
                elif player_turn == 2:
                    self.playerTwoAtoms.append(tuple([row-1, column]))
                self.checkForRowAndColumn(row-1, column, player_turn)
                self.grid[row+1][column] += 1
                self.deleteTheAtom(row+1, column)
                if player_turn == 1:
                    self.playerOneAtoms.append(tuple([row+1, column]))
                elif player_turn == 2:
                    self.playerTwoAtoms.append(tuple([row+1, column]))
                self.checkForRowAndColumn(row+1, column, player_turn)
                self.grid[row][column-1] += 1
                self.deleteTheAtom(row, column-1)
                if player_turn == 1:
                    self.playerOneAtoms.append(tuple([row, column-1]))
                elif player_turn == 2:
                    self.playerTwoAtoms.append(tuple([row, column-1]))
                self.checkForRowAndColumn(row, column-1, player_turn)


        if (column == 0 and row >= 1 and row <= 7):
            if self.grid[row][column] == 3:
                self.grid[row][column] = 0
                self.deleteTheAtom(row, column)
                self.grid[row-1][column] += 1
                self.deleteTheAtom(row-1, column)
                if player_turn == 1:
                    self.playerOneAtoms.append(tuple([row-1, column]))
                elif player_turn == 2:
                    self.playerTwoAtoms.append(tuple([row-1, column]))
                self.checkForRowAndColumn(row-1, column, player_turn)
                self.grid[row+1][column] += 1
                self.deleteTheAtom(row+1, column)
                if player_turn == 1:
                    self.playerOneAtoms.append(tuple([row+1, column]))
                elif player_turn == 2:
                    self.playerTwoAtoms.append(tuple([row+1, column]))
                self.checkForRowAndColumn(row+1, column, player_turn)
                self.grid[row][column+1] += 1
                self.deleteTheAtom(row, column+1)
                if player_turn == 1:
                    self.playerOneAtoms.append(tuple([row, column+1]))
                elif player_turn == 2:
                    self.playerTwoAtoms.append(tuple([row, column+1]))
                self.checkForRowAndColumn(row, column+1, player_turn)

        else:
            self.checkForTheFour(row, column, player_turn)

    def checkForWin(self, turn):

        #Need to add the value of win in the database

        if len(self.playerOneAtoms) == 0 and turn > 2:
            #Player two won
            print("Player 2 won")
            self.win_check = 2
            player_name = self.play2
            print("Player name is: ", self.play1)
            mycursor.execute("use gameserver;")
            win_string = "UPDATE user SET win = win+1 WHERE name=\"" + self.play1+"\";"
            loss_string = "UPDATE user SET loss = loss+1 WHERE name=\"" + self.play2+"\";"
            mycursor.execute(win_string)
            mycursor.execute(loss_string)
            adding_move_string = "INSERT INTO games (player1,player2,move1,move2) VALUES (\""+self.play1+"\",\""+self.play2+"\",\""+str(self.playerOneMoves)+"\",\""+str(self.playerTwoMoves)+"\");"            
            print(adding_move_string)
            mycursor.execute(adding_move_string)
            mycursor.execute("commit;")


        elif len(self.playerTwoAtoms) == 0 and turn > 2:
            #player one won
            print("Player 1 won")
            self.win_check = 1
            player_name = self.play1
            print("Player name is: ", self.play2)
            mycursor.execute("use gameserver;")
            win_string = "UPDATE user SET win = win+1 WHERE name=\"" + self.play2+"\";"
            loss_string = "UPDATE user SET loss = loss+1 WHERE name=\"" + self.play1+"\";"
            mycursor.execute(win_string)
            mycursor.execute(loss_string)
            adding_move_string = "INSERT INTO games (player1,player2,move1,move2) VALUES (\""+self.play1+"\",\""+self.play2+"\",\""+str(self.playerOneMoves)+"\",\""+str(self.playerTwoMoves)+"\");"
            print(adding_move_string)
            mycursor.execute(adding_move_string)
            mycursor.execute("commit;")

        
        else:
            print("The game is still going on")
            self.win_check = 0



    def checkForTheFour(self, row, column, player_turn):
        if self.grid[row][column] == 4:
            self.grid[row][column] = 0
            self.deleteTheAtom(row, column)
            self.grid[row+1][column] += 1
            self.deleteTheAtom(row+1, column)
            if player_turn == 1:
                self.playerOneAtoms.append(tuple([row+1, column]))
            elif player_turn == 2:
                self.playerTwoAtoms.append(tuple([row+1, column]))
            self.checkForRowAndColumn(row+1, column, player_turn)
            self.grid[row][column+1] += 1
            self.deleteTheAtom(row, column+1)
            if player_turn == 1:
                self.playerOneAtoms.append(tuple([row, column+1]))
            elif player_turn == 2:
                self.playerTwoAtoms.append(tuple([row, column+1]))
            self.checkForRowAndColumn(row, column+1, player_turn)
            self.grid[row-1][column] += 1
            self.deleteTheAtom(row-1, column)
            if player_turn == 1:
                self.playerOneAtoms.append(tuple([row-1, column]))
            elif player_turn == 2:
                self.playerTwoAtoms.append(tuple([row-1, column]))  
            self.checkForTheFour(row-1, column, player_turn)
            self.grid[row][column-1] += 1
            self.deleteTheAtom(row, column-1)
            if player_turn == 1:
                self.playerOneAtoms.append(tuple([row, column-1]))
            elif player_turn == 2:
                self.playerTwoAtoms.append(tuple([row, column-1]))
            self.checkForRowAndColumn(row, column-1, player_turn)

    
    def check_grid(self, grid_data, atom1, atom2):
        flag = 1
        for i in range(10):
            for j in range(10):
                if grid_data[i][j] > 3 or grid_data[i][j] < 0:
                    flag= 0
        
        for x in atom1:
            if x[0] < 0 or x[0] > 9 or x[1] < 0 or x[1] > 9:
                flag = 0 

        for x in atom2:
            if x[0] < 0 or x[0] > 9 or x[1] < 0 or x[1] > 9:
                flag = 0
        
        if flag == 0:
            return False
        return True
        

    def run(self):

        
        player1 = connbuffer[self.play1]
        player2 = connbuffer[self.play2]
        updated_player1 = self.play1
        updated_player2 = self.play2
        first = self.play1

        data = pickle.dumps("Ready")
        player1.send(data)
        player2.send(data)
        data = pickle.dumps(self.play1)
        player2.send(data)
        data = pickle.dumps(self.play2)
        player1.send(data)
        data = pickle.dumps(first)
        player1.send(data)
        player2.send(data)
        counter = 0
        win_player = 0
        turn = 1
        try: 
            while True:
                ok = 0
                self.checkForWin(counter)
                # print("DEBUG: Both the players should get this")
                print("Value of win_player is: \n", win_player)
                if turn%2 == 1:
                    #New dictionary
                    print("DEBUG: My name is: ", str(player1))
                    signal_and_data = []
                    signal_and_data.append(0)
                    signal_and_data.append(self.playerTwoAtoms)
                    signal_and_data.append(self.grid)
                    signal_and_data.append(self.playerOneAtoms)
                    signal_and_data.append(self.win_check)

                    try:
                        player2.send(pickle.dumps(signal_and_data))
                    except:
                        print("Conn error, remove play2 conn and try reconnection 1")
                        lock_buf.acquire()
                        ele = connbuffer.pop(updated_player2, "Not found")
                        lock_buf.release() 
                        print(updated_player2+" removed")
                        connected = False
                        tic = time.time()
                        tac = time.time()
                        while not connected and (tac-tic) < 300:
                            try:
                                
                                if updated_player2 in connbuffer:
                                    print(updated_player2 + " Readded")
                                    player2 = connbuffer[updated_player2]
                                    player2.send(pickle.dumps("Ready"))
                                    player2.send(pickle.dumps(updated_player1))
                                    player2.send(pickle.dumps(updated_player1))
                                    player2.send(pickle.dumps(signal_and_data))
                                    connected = True
                                else:
                                    time.sleep(5)
                                    tac = time.time()
                            except:
                                lock_buf.acquire()
                                ele = connbuffer.pop(updated_player2, "Not found")
                                lock_buf.acquire()

                                time.sleep(5)
                                tac = time.time()
                        if (tac-tic) >= 300 or not connected:
                            winner = 1
                            break

                            
                                

                    signal_and_data[0] = 1
                    try:
                        player1.send(pickle.dumps(signal_and_data))
                    
                    except:
                        print("Conn error, remove play1 conn and try reconnection 2")
                        lock_buf.acquire()
                        ele = connbuffer.pop(updated_player1, "Not found")
                        lock_buf.release() 
                        print(updated_player1+" removed")
                        connected = False
                        tic = time.time()
                        tac = time.time()
                        while not connected and (tac-tic) < 300:
                            try:
                                
                                if updated_player1 in connbuffer:
                                    print(updated_player2+" readded")
                                    player1 = connbuffer[updated_player1]
                                    player1.send(pickle.dumps("Ready"))
                                    player1.send(pickle.dumps(updated_player1))
                                    player1.send(pickle.dumps(updated_player1))
                                    player1.send(pickle.dumps(signal_and_data))
                                    connected = True
                                else:
                                    time.sleep(5)
                                    tac = time.time()
                            except:
                                lock_buf.acquire()
                                ele = connbuffer.pop(updated_player1, "Not found")
                                lock_buf.acquire()
                                
                                time.sleep(5)
                                tac = time.time()

                        if (tac-tic) >= 300 or not connected:
                            winner = 2
                            break


                    print("Data sent to player 1\n")

                    try:
                        recvdata = player1.recv(1024)
                    except timeout:
                        print("timeout")
                        winner = 2
                        break
                    except error:
                        print("Conn error, remove play1 conn and try reconnection 3")
                        lock_buf.acquire()
                        ele = connbuffer.pop(updated_player1, "Not found")
                        lock_buf.release() 
                        print(updated_player1+" removed")
                        connected = False
                        tic = time.time()
                        tac = time.time()
                        while not connected and (tac-tic) < 300:
                            try:
                                
                                if updated_player1 in connbuffer:
                                    print(updated_player2+" readded")
                                    player1 = connbuffer[updated_player1]
                                    player1.send(pickle.dumps("Ready"))
                                    player1.send(pickle.dumps(updated_player1))
                                    player1.send(pickle.dumps(updated_player1))
                                    player1.send(pickle.dumps(signal_and_data))
                                    recvdata = player1.recv(1024)
                                    connected = True
                                else:
                                    time.sleep(5)
                                    tac = time.time()
                            except:
                                lock_buf.acquire()
                                ele = connbuffer.pop(updated_player1, "Not found")
                                lock_buf.acquire()
                                
                                time.sleep(5)
                                tac = time.time()
                        if (tac-tic) >= 300 or not connected:
                            winner = 2
                            break

                    #for dos prevention, we quit game if data received is less than 10 bytes
                    if len(recvdata) < 10:
                        winner = 2
                        break

                    recv_data = pickle.loads(recvdata)
                    print("Data recieved by Player 1\n")
                    print(recv_data)

                    #After we've recieved the data first we will need to compute 
                    # everything and make changes to our grid locally
                    if recv_data[0] == 1:
                        print("Conn error, remove play1 conn and try reconnection 4")
                        lock_buf.acquire()
                        ele=connbuffer.pop(updated_player1, "Not found")
                        lock_buf.release()
                        print(updated_player1+" removed") 
                        connected = False
                        tic = time.time()
                        tac = time.time()
                        while not connected and (tac-tic) < 300:
                            try:
                                if updated_player1 in connbuffer:
                                    print(updated_player1+" readded")
                                    player1=connbuffer[updated_player1]
                                    player1.send(pickle.dumps("Ready"))
                                    player1.send(pickle.dumps(updated_player1))
                                    player1.send(pickle.dumps(updated_player1))
                                    player1.send(pickle.dumps(signal_and_data))
                                    recvdata = player1.recv(1024)
                                    connected = True
                                else:
                                    time.sleep(5)
                                    tac = time.time()
                            except:
                                lock_buf.acquire()
                                ele = connbuffer.pop(updated_player1, "Not found")
                                lock_buf.acquire()
                                time.sleep(5)
                                tac = time.time()
                        if (tac-tic) >= 300 or not connected:
                            winner = 2
                            break
                            
                        print("DEBUG: player 1 clicked on the exit button")
                        #this the quit command, this client has exited the game
                        print("This player wants to quit the game")
                    if recv_data[0] == 2:
                        #This is the mousebutton command
                        print("DEBUG: Player 1 click on one of the cell")
                        column = recv_data[5]
                        row = recv_data[4]

                        string_to_append = str(turn)+":("+str(column)+","+str(row)+")"

                        self.playerOneMoves.append(string_to_append)
                        
                        print("DEBUG: row ", row, " and column ", column, "were obtained")

                        if (row, column) in self.playerTwoAtoms:
                            print("DEBUG: row and column exists in player two")
                            print("You can't click there")
                        else:
                            if (row, column) in self.playerOneAtoms:
                                print("It is already in the block")   
                                # Set that location to one
                                self.grid[row][column] += 1
                                #turn = turn + 1
                                self.checkForRowAndColumn(row, column, 1)
                                # print("Click ", pos, "Grid coordinates: ", row, column)
                                print("thisPlayerAtoms are: ", self.playerOneAtoms)
                                print("otherPlayerAtoms are: ", self.playerTwoAtoms)

                            else:
                                self.playerOneAtoms.append(tuple([row, column]))
                                # Set that location to one
                                self.grid[row][column] += 1
                                #turn = turn + 1
                                self.checkForRowAndColumn(row, column, 1)
                                # print("Click ", pos, "Grid coordinates: ", row, column)
                                print("thisPlayerAtoms are: ", self.playerOneAtoms)
                                print("otherPlayerAtoms are: ", self.playerTwoAtoms)
  
                    #processing grid data
                    turn = turn+1
                    counter = counter+1
                    grid_data = recv_data[3]
                    flag = 1
                    if not self.check_grid(grid_data, recv_data[1], recv_data[2]):
                        flag = 0
                    
                    #add the function to cross check grid here 
                    if recv_data[3] == self.grid:
                        print("It is correct")
                    else:
                        print("It is incorrect")
                        flag=0
                        ok = -1
                    

                    print("DEBUG: Ok value is: ", ok)
                    player1.send(pickle.dumps(ok))
                    
                    #player1.send(pickle.dumps(flag))
                    # player1.send(pickle.dumps(1))
                    #recvdata = player2.recv(1024)
                    #if pickle.loads(recvdata) ==1:
                    #Here I have to send the data to player 2 to say that your waiting is over now
                    # player2.send(pickle.dumps(1))
                else:
                    #New dictionary
                    signal_and_data = []
                    signal_and_data.append(0)
                    signal_and_data.append(self.playerOneAtoms)
                    signal_and_data.append(self.grid)
                    signal_and_data.append(self.playerTwoAtoms)
                    signal_and_data.append(self.win_check)
                    try:
                        player1.send(pickle.dumps(signal_and_data))
                    except:
                        print("Conn error, remove play1 conn and try reconnection 5")
                        lock_buf.acquire()
                        ele=connbuffer.pop(updated_player1,"Not found")
                        lock_buf.release() 
                        print(updated_player1+" removed")
                        connected = False
                        tic = time.time()
                        tac = time.time()
                        while not connected and (tac-tic) < 300:
                            try:
                                
                                if updated_player1 in connbuffer:
                                    print(updated_player1+" readded")
                                    player1 = connbuffer[updated_player1]
                                    player1.send(pickle.dumps("Ready"))
                                    player1.send(pickle.dumps(updated_player1))
                                    player1.send(pickle.dumps(updated_player1))
                                    player1.send(pickle.dumps(signal_and_data))
                                    connected = True
                                else:
                                    time.sleep(5)
                                    tac = time.time()
                            except:
                                lock_buf.acquire()
                                ele = connbuffer.pop(updated_player1, "Not found")
                                lock_buf.acquire()
                                
                                time.sleep(5)
                                tac = time.time()

                        if (tac-tic) >= 300 or not connected:
                            winner = 2
                            break
                    
                    
                    
                    signal_and_data[0] = 1
                    try:
                        player2.send(pickle.dumps(signal_and_data))
                    except:
                        print("Conn error, remove play2 conn and try reconnection 6")
                        lock_buf.acquire()
                        ele = connbuffer.pop(updated_player2, "Not found")
                        lock_buf.release() 
                        print(updated_player2+" removed")
                        connected = False
                        tic = time.time()
                        tac = time.time()
                        while not connected and (tac-tic) < 300:
                            try:                                
                                if updated_player2 in connbuffer:
                                    print(updated_player2+" removed")
                                    player2 = connbuffer[updated_player2]
                                    player2.send(pickle.dumps("Ready"))
                                    player2.send(pickle.dumps(updated_player1))
                                    player2.send(pickle.dumps(updated_player1))
                                    player2.send(pickle.dumps(signal_and_data))
                                    connected = True
                                else:
                                    time.sleep(5)
                                    tac = time.time()
                            except:
                                lock_buf.acquire()
                                ele = connbuffer.pop(updated_player2, "Not found")
                                lock_buf.acquire()
                                time.sleep(5)
                                tac = time.time()
                        if (tac-tic) >= 300 or not connected:
                            winner = 1
                            break

                    print("Data sent to player 2\n")
                    try:
                        recvdata = player2.recv(1024)
                    except timeout:
                        print("Timeout")
                        winner = 1
                        break
                    except error:
                        print("Conn error, remove play2 conn and try reconnection 7")
                        lock_buf.acquire()
                        ele = connbuffer.pop(updated_player2, "Not found")
                        lock_buf.release() 
                        print(updated_player2+" removed")
                        connected = False
                        tic = time.time()
                        tac = time.time()
                        while not connected and (tac-tic) < 300:
                            try:
                                
                                if updated_player2 in connbuffer:
                                    print(updated_player2+" readded")
                                    player2 = connbuffer[updated_player2]
                                    player2.send(pickle.dumps("Ready"))
                                    player2.send(pickle.dumps(updated_player1))
                                    player2.send(pickle.dumps(updated_player1))
                                    player2.send(pickle.dumps(signal_and_data))
                                    recvdata = player2.recv(1024)
                                    connected = True
                                else:
                                    time.sleep(5)
                                    tac = time.time()
                            except:
                                lock_buf.acquire()
                                ele = connbuffer.pop(updated_player2, "Not found")
                                lock_buf.acquire()

                                time.sleep(5)
                                tac = time.time()
                        if (tac-tic) >= 300 or not connected:
                            winner = 1
                            break
                    #for dos prevention, drop game if packet is less than 10 bytes
                    if len(recvdata) < 10:
                        winner = 1
                        break
                    recv_data = pickle.loads(recvdata)
                    print("Data recieved by Player 2\n")
                    print(recv_data)
                    
                    #After we've recieved the data first we will need to compute everything and make changes to our grid locally
                    if recv_data[0] == 1:
                        print("Conn error, remove play2 conn and try reconnection 8 ")
                        lock_buf.acquire()
                        ele = connbuffer.pop(updated_player2, "Not found")
                        lock_buf.release() 
                        print(updated_player2+" removed")
                        connected = False
                        tic = time.time()
                        tac = time.time()
                        while not connected and (tac-tic) < 300:
                            try:
                                
                                if updated_player2 in connbuffer:
                                    print(updated_player2+ " readded")
                                    player2 = connbuffer[updated_player2]
                                    player2.send(pickle.dumps("Ready"))
                                    player2.send(pickle.dumps(updated_player1))
                                    player2.send(pickle.dumps(updated_player1))
                                    player2.send(pickle.dumps(signal_and_data))
                                    recvdata = player2.recv(1024)
                                    connected = True
                                else:
                                    time.sleep(5)
                                    tac = time.time()
                            except:
                                lock_buf.acquire()
                                ele = connbuffer.pop(updated_player2, "Not found")
                                lock_buf.acquire()

                                time.sleep(5)
                                tac = time.time()
                        if (tac-tic) >= 300 or not connected:
                            winner = 1
                            break
                        #this the quit command, this client has exited the game
                        print("This player wants to quit the game")
                    if recv_data[0] == 2:
                        #This is the mousebutton command
                        print("DEBUG: Inside Player 2:  Player 2 has clicked on a cell")
                        column = recv_data[5]
                        row = recv_data[4]
                        string_to_append = str(turn)+":("+str(column)+","+str(row)+")"

                        self.playerTwoMoves.append(string_to_append)

                        print("DEBUG: Column ", column, " and Row ", row, "was recieved from player two")
                        if (row, column) in self.playerOneAtoms:
                            print("You can't click there")
                        else:
                            if (row, column) in self.playerTwoAtoms:
                                print("It is already in the block")  
                                # Set that location to one
                                self.grid[row][column] += 1
                                #turn = turn + 1
                                self.checkForRowAndColumn(row, column, 2)
                                # print("Click ", pos, "Grid coordinates: ", row, column)
                                print("thisPlayerAtoms are: ", self.playerOneAtoms)
                                print("otherPlayerAtoms are: ", self.playerTwoAtoms)
                            else:
                                self.playerTwoAtoms.append(tuple([row, column]))
                                # Set that location to one
                                self.grid[row][column] += 1
                                #turn = turn + 1
                                self.checkForRowAndColumn(row, column, 2)
                                # print("Click ", pos, "Grid coordinates: ", row, column)
                                print("thisPlayerAtoms are: ", self.playerOneAtoms)
                                print("otherPlayerAtoms are: ", self.playerTwoAtoms)
                                
                    print("Data recieved from player 2\n")
                    print(recv_data)

                    #processing grid data
                    turn = turn+1
                    counter = counter+1
                    grid_data = recv_data[3]
                    flag = 1
                    if not self.check_grid(grid_data, recv_data[1], recv_data[2]):
                        flag = 0
                    
                    #add the function to cross check grid here 
                    if recv_data[3] == self.grid:
                        print("It is correct")
                    else:
                        print("It is incorrect")

                        flag = 0
                        ok = -1

                    #player2.send(pickle.dumps(flag))
                    # player2.send(pickle.dumps(1))
                    # player2.send(recvdata)
                    #recvdata = player2.recv(1024)
                    #if pickle.loads(recvdata) ==1:
                    #Sending the data to player 2 let it know that you can resume now
                    player2.send(pickle.dumps(ok))
        finally:
            print("Game has ended")
            
            try:
                player1.close()
            except:
                print("Error dropping connection")
            try: 
                player2.close()
            except:
                print("Error dropping connection")

            occupied_ports.remove(userlist[self.play1][2])
            occupied_ports.remove(userlist[self.play2][2])

            lock_buf.acquire()
            element1 = connbuffer.pop(self.play1, "nf")
            element1 = connbuffer.pop(self.play2, "nf")
            if element1 == "nf":
                print("Error removing from connbuffer")
            
            element2 = userlist.pop(self.play1, "nf")
            element2 = userlist.pop(self.play2, "nf")
            if element2 == "nf":
                print("Error removing from userlist")
            lock_buf.release()

room = Thread(target=room_creator, args=())
room.start()

server = socket(AF_INET, SOCK_STREAM)
server.bind((LOCALHOST, server_port))
server.listen(50)

while True:
    
    connection, client_address = server.accept()
    connstream = ssl.wrap_socket(connection, server_side=True, certfile="server.crt", keyfile="server.key")
    try:
        sentence = connstream.recv(1024)
        
        if sentence:
            if len(sentence) < 10:
                connstream.close()
                continue
            data = pickle.loads(sentence)
            data_send = 1
            if len(data) != 5:
                data_send = -2
            elif namereg.match(data[1]) is None or regpass.match(data[2]) is None:
                #username or passord format is incorrect
                data_send = -2
            elif data[0] == "logon":
                mycursor.execute("SELECT * FROM user WHERE name = %s;", (data[1],))
                x = mycursor.fetchone()
                if x is None:
                    hash_pw = hash_password(data[2])
                    val_recv = (data[1], hash_pw, 0, 0, 0)
                    sql = "INSERT INTO user (name, password,win,loss,draw) VALUES (%s, %s,%s, %s, %s);"
                    mycursor.execute(sql, val_recv)
                    mydb.commit()
                    mycursor.execute("SELECT * FROM user WHERE name = %s;", (data[1],))
                    x = mycursor.fetchone()
                    print(x)
                    
                    ipand = []
                    ipand.append(data[2])
                    ipand.append(data[3])

                    if ports > 64000:
                        ports = 60000
                    while ports in occupied_ports:
                        ports = ports+1    
                    
                    occupied_ports.append(ports)
                    ipand.append(ports)
                    #ipand.append(1)
                    userlist[data[1]] = ipand
                    currport = ports
                    currname = data[1]
                    ports = ports+1
                    data_send = 1
                else:
                    #username is already present
                    data_send = -1
            elif data[0] == "login":
                mycursor.execute("SELECT * FROM user WHERE name = %s;", (data[1],))
                x = mycursor.fetchone()
                if x is None:
                    #username is not in data base for login
                    data_send = -3
                else :
                    temp_hash = x[1]
                    if verify_password(x[1], data[2]):
                        if data[1] not in userlist:
                            ipand = []
                            ipand.append(data[2])
                            ipand.append(data[3])
                            if ports > 64000:
                                ports = 60000
                            while ports in occupied_ports:
                                ports = ports+1    
                            
                            occupied_ports.append(ports)
                            ipand.append(ports)
                            #ipand.append(1)
                            userlist[data[1]] = ipand
                            currport = ports
                            currname = data[1]
                            ports = ports
                            data_send = 1
                        else:
                            if data[1] in connbuffer:
                                data_send = -1
                            else:
                                currport = userlist[data[1]][2]
                                currname = data[1]
                                data_send = 2  
                    else:
                        #password is incorrect
                        data_send = -4
        
            print("Recieved = "+client_address[0]+" : "+str(client_address[1]))
            if data_send != 1 and data_send != 2:
                currport = data_send        
            sentence = pickle.dumps(currport)
            connstream.send(sentence)
        
        connstream.close()
        if data_send == 1:
            t = Thread(target=client_specific_server, args=(currport, currname, 1,))
            t.start()
        elif data_send == 2:
            t = Thread(target=client_specific_server, args=(currport, currname, 2,))
            t.start()

    except:
        print("Connection Error")
        try:
            connstream.close()
        except:
            print("connection error")

        #sys.exit(0)
        