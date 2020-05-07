import pickle, re, time, random, sys, ssl
from socket import *

from threading import Thread, Lock

ports=60000
namereg=re.compile("^[a-zA-Z0-9]{0,20}$")
LOCALHOST="127.0.0.1"
server_port= 49999

buffer=[]
connbuffer={}

userlist={}
occupied_ports=[]
gamerooms=[]

lock_buf=Lock()

playerOneAtoms = []
playerTwoAtoms = []
grid = []
    
for row in range(10):
    grid.append([])
    for column in range(10):
        grid[row].append(0)  

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 40
HEIGHT = 40
 
# This sets the margin between each cell
MARGIN = 5

#defining turn
turn = 0

def deleteTheAtom(row, column):
    if (row, column) in playerOneAtoms:
        playerOneAtoms.remove(tuple([row, column]))
    if (row, column) in playerTwoAtoms:
        playerTwoAtoms.remove(tuple([row, column]))


def checkForRowAndColumn(row, column, player_turn):
    if (row == 0 and column == 0):
        #We have to burst at two
        if(grid[row][column] == 2):
            grid[row][column] = 0
            grid[row+1][column] += 1
            deleteTheAtom(row+1, column)
            if player_turn == 1:
                playerOneAtoms.append(tuple([row+1, column]))
            elif player_turn == 2:
                playerTwoAtoms.append(tuple([row+1, column]))
            checkForRowAndColumn(row+1, column, player_turn)
            grid[row][column+1] += 1
            deleteTheAtom(row, column+1)
            if player_turn == 1:
                playerOneAtoms.append(tuple([row, column+1]))
            elif player_turn == 2:
                playerTwoAtoms.append(tuple([row, column+1]))
            checkForRowAndColumn(row, column+1, player_turn)

    if (row == 9 and column == 0):
        #We have to burst at two
        if(grid[row][column] == 2):
            grid[row][column] = 0
            grid[row-1][column] += 1
            deleteTheAtom(row-1, column)
            if player_turn == 1:
                playerOneAtoms.append(tuple([row-1, column]))
            elif player_turn == 2:
                playerTwoAtoms.append(tuple([row-1, column]))
            checkForRowAndColumn(row-1, column, player_turn)
            grid[row][column+1] += 1
            deleteTheAtom(row, column+1)
            if player_turn == 1:
                playerOneAtoms.append(tuple([row, column+1]))
            elif player_turn == 2:
                playerTwoAtoms.append(tuple([row+1, column+1]))
            checkForRowAndColumn(row, column+1, player_turn)

    if (row == 0 and column == 9):
        if(grid[row][column] == 2):
            grid[row][column] = 0
            grid[row+1][column] += 1
            deleteTheAtom(row+1, column)
            if player_turn == 1:
                playerOneAtoms.append(tuple([row+1, column]))
            elif player_turn == 2:
                playerTwoAtoms.append(tuple([row+1, column]))
            checkForRowAndColumn(row+1, column, player_turn)
            grid[row][column-1] += 1
            deleteTheAtom(row, column-1)
            if player_turn == 1:
                playerOneAtoms.append(tuple([row, column-1]))
            elif player_turn == 2:
                playerTwoAtoms.append(tuple([row+1, column-1]))
            checkForRowAndColumn(row, column-1, player_turn)


    if (row == 9 and column == 9):
        if(grid[row][column] == 2):
            grid[row][column] = 0
            grid[row-1][column] += 1
            deleteTheAtom(row-1, column)
            if player_turn == 1:
                playerOneAtoms.append(tuple([row-1, column]))
            elif player_turn == 2:
                playerTwoAtoms.append(tuple([row-1, column]))
            checkForRowAndColumn(row-1, column, player_turn)
            grid[row][column-1] += 1
            deleteTheAtom(row, column-1)
            if player_turn == 1:
                playerOneAtoms.append(tuple([row, column-1]))
            elif player_turn == 2:
                playerTwoAtoms.append(tuple([row, column-1]))
            checkForRowAndColumn(row, column-1, player_turn)

    if (row == 0 and column >=1 and column <=8):
        #We now check for three
        if(grid[row][column] == 3):
            grid[row][column] = 0
            grid[row+1][column] += 1
            deleteTheAtom(row+1, column)
            if player_turn == 1:
                playerOneAtoms.append(tuple([row+1, column]))
            elif player_turn == 2:
                playerTwoAtoms.append(tuple([row+1, column]))
            checkForRowAndColumn(row+1, column, player_turn)
            grid[row][column+1] += 1
            deleteTheAtom(row, column+1)
            if player_turn == 1:
                playerOneAtoms.append(tuple([row, column+1]))
            elif player_turn == 2:
                playerTwoAtoms.append(tuple([row, column+1]))
            checkForRowAndColumn(row, column+1, player_turn)
            grid[row][column-1] += 1
            deleteTheAtom(row, column-1)
            if player_turn == 1:
                playerOneAtoms.append(tuple([row, column-1]))
            elif player_turn == 2:
                playerTwoAtoms.append(tuple([row, column-1]))
            checkForRowAndColumn(row, column-1, player_turn)

    if (row == 9 and column >=1 and column <=8):
        if(grid[row][column] == 3):
            grid[row][column] = 0
            grid[row-1][column] += 1
            deleteTheAtom(row-1, column)
            if player_turn == 1:
                playerOneAtoms.append(tuple([row-1, column]))
            elif player_turn == 2:
                playerTwoAtoms.append(tuple([row-1, column]))
            checkForRowAndColumn(row-1, column, player_turn)
            grid[row][column+1] += 1
            deleteTheAtom(row, column+1)
            if player_turn == 1:
                playerOneAtoms.append(tuple([row, column+1]))
            elif player_turn == 2:
                playerTwoAtoms.append(tuple([row, column+1]))
            checkForRowAndColumn(row, column+1, player_turn)
            grid[row][column-1] += 1
            deleteTheAtom(row, column-1)
            if player_turn == 1:
                playerOneAtoms.append(tuple([row, column-1]))
            elif player_turn == 2:
                playerTwoAtoms.append(tuple([row, column-1]))
            checkForRowAndColumn(row, column-1, player_turn)

    if (column == 9 and row >=1 and row <=8):
        if(grid[row][column] == 3):
            grid[row][column] = 0
            grid[row-1][column] += 1
            deleteTheAtom(row-1, column)
            if player_turn == 1:
                playerOneAtoms.append(tuple([row-1, column]))
            elif player_turn == 2:
                playerTwoAtoms.append(tuple([row-1, column]))
            checkForRowAndColumn(row-1, column, player_turn)
            grid[row+1][column] += 1
            deleteTheAtom(row+1, column)
            if player_turn == 1:
                playerOneAtoms.append(tuple([row+1, column]))
            elif player_turn == 2:
                playerTwoAtoms.append(tuple([row+1, column]))
            checkForRowAndColumn(row+1, column, player_turn)
            grid[row][column-1] += 1
            deleteTheAtom(row, column-1)
            if player_turn == 1:
                playerOneAtoms.append(tuple([row, column-1]))
            elif player_turn == 2:
                playerTwoAtoms.append(tuple([row, column-1]))
            checkForRowAndColumn(row, column-1, player_turn)


    if (column == 0 and row >=1 and row <=8):
        if(grid[row][column] == 3):
            grid[row][column] = 0
            grid[row-1][column] += 1
            deleteTheAtom(row-1, column)
            if player_turn == 1:
                playerOneAtoms.append(tuple([row-1, column]))
            elif player_turn == 2:
                playerTwoAtoms.append(tuple([row-1, column]))
            checkForRowAndColumn(row-1, column, player_turn)
            grid[row+1][column] += 1
            deleteTheAtom(row+1, column)
            if player_turn == 1:
                playerOneAtoms.append(tuple([row+1, column]))
            elif player_turn == 2:
                playerTwoAtoms.append(tuple([row+1, column]))
            checkForRowAndColumn(row+1, column, player_turn)
            grid[row][column+1] += 1
            deleteTheAtom(row, column+1)
            if player_turn == 1:
                playerOneAtoms.append(tuple([row, column+1]))
            elif player_turn == 2:
                playerTwoAtoms.append(tuple([row, column+1]))
            checkForRowAndColumn(row, column+1, player_turn)

    else:
        checkForTheFour(row, column, player_turn)

done = False

def checkForWin():
    if(len(playerOneAtoms) == 0):
        #Player 2 has won, end the game
        print("Player 2 won")
    elif(len(playerTwoAtoms) == 0):
        #Player 1 has won, end the game
        print("Player 1 won")
    else:
        #Game is still going on, continue
        return  


def checkForTheFour(row, column, player_turn):
    if(grid[row][column] == 4):
        grid[row][column] = 0
        grid[row+1][column] += 1
        deleteTheAtom(row+1, column)
        if player_turn == 1:
            playerOneAtoms.append(tuple([row+1, column]))
        elif player_turn == 2:
            playerTwoAtoms.append(tuple([row+1, column]))
        checkForRowAndColumn(row+1, column, player_turn)
        grid[row][column+1] += 1
        deleteTheAtom(row, column+1)
        if player_turn == 1:
            playerOneAtoms.append(tuple([row, column+1]))
        elif player_turn == 2:
            playerTwoAtoms.append(tuple([row, column+1]))
        checkForRowAndColumn(row, column+1, player_turn)
        grid[row-1][column] += 1
        deleteTheAtom(row-1, column)
        if player_turn == 1:
            playerOneAtoms.append(tuple([row-1, column]))
        elif player_turn == 2:
            playerTwoAtoms.append(tuple([row-1, column]))  
        checkForTheFour(row-1, column, player_turn)
        grid[row][column-1] += 1
        deleteTheAtom(row, column-1)
        if player_turn == 1:
            playerOneAtoms.append(tuple([row, column-1]))
        elif player_turn == 2:
            playerTwoAtoms.append(tuple([row, column-1]))
        checkForRowAndColumn(row, column-1, player_turn)

def client_specific_server(portn, clientname):
    lhost="127.0.0.1"
    port= portn
    print(clientname)
    serversock = socket(AF_INET, SOCK_STREAM)
    serversock.bind((lhost, port))
    serversock.listen(1)
    #while True:
    connect, clientadd = serversock.accept()
    connssl = ssl.wrap_socket(connect,server_side=True,certfile="server.crt", keyfile="server.key")
    
    inputd = connssl.recv(1024)
    #data = pickle.loads(inputd)

    sentence=pickle.dumps("You are added in Buffer")
    connssl.send(sentence)
    lock_buf.acquire()
    buffer.append(clientname)
    connbuffer[clientname]=connssl
    lock_buf.release()
    #connbuffer[clientname].close()


def room_creator():
    while True:
        time.sleep(5)
        lock_buf.acquire()
        n=len(buffer)
        if n<2:
            lock_buf.release()
            for c in buffer:
                data=pickle.dumps("Waiting for another user")
                connbuffer[c].send(data)
        elif n==0:
            lock_buf.release()

        else:
            for i in range(0,n,2):
                if i+1 != n:
                    #rmo=Thread(target=player_game_room, args=(buffer[i],buffer[i+1],))
                    rmo=player_game_room(buffer[i],buffer[i+1])
                    print("Thread is running "+str(i)+" "+str(i+1)+" "+str(n))
                    rmo.start()
            if n%2==1:
                last=buffer[n-1]
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
        self.play1=play1
        self.play2=play2

    def check_grid(self, grid_data, atom1, atom2):
        flag=1
        for i in range(10):
            for j in range(10):
                if grid_data[i][j] > 3 or grid_data[i][j] < 0:
                    flag=0
        
        for x in atom1:
            if x[0]<0 or x[0]>9 or x[1]<0 or x[1]>9:
                flag=0 

        for x in atom2:
            if x[0]<0 or x[0]>9 or x[1]<0 or x[1]>9:
                flag=0
        
        if flag == 0:
            return False
        else:
            return True
        


    def run(self):

        if random.randrange(1,3) == 1:
            player1=connbuffer[self.play1]
            player2=connbuffer[self.play2]
            first=self.play1
        else:
            player2=connbuffer[self.play1]
            player1=connbuffer[self.play2]
            first=self.play2

        data=pickle.dumps("Ready")
        player1.send(data)
        player2.send(data)
        data=pickle.dumps(self.play1)
        player2.send(data)
        data=pickle.dumps(self.play2)
        player1.send(data)
        data=pickle.dumps(first)
        player1.send(data)
        player2.send(data)

        count=1
        while True:
            print("This executes\n")
            if count%2 == 1:
                #New dictionary
                signal_and_data = []
                signal_and_data.append(0)
                signal_and_data.append(playerTwoAtoms)
                player2.send(pickle.dumps(signal_and_data))
                signal_and_data[0] = 1
                player1.send(pickle.dumps(signal_and_data))
                print("Data sent to player 1\n")
                recv_data=pickle.loads(recvdata)
                print("Data recieved by Player 1\n")
                #After we've recieved the data first we will need to compute everything and make changes to our grid locally
                if recv_data[0] == 1:
                    #this the quit command, this client has exited the game
                    print("This player wants to quit the game")
                if recv_data[0] == 2:
                    #This is the mousebutton command

                    column = recv_data[5]
                    row = recv_data[4]

                    if (row, column) in playerTwoAtoms:
                        print("You can't click there")
                    else:
                        if (row, column) in playerOneAtoms:
                            print("It is already in the block")   
                            # Set that location to one
                            grid[row][column] += 1
                            turn = turn + 1
                            checkForRowAndColumn(row, column, 1)
                            # print("Click ", pos, "Grid coordinates: ", row, column)
                            print("thisPlayerAtoms are: ", playerOneAtoms)
                            print("otherPlayerAtoms are: ", playerTwoAtoms)

                        else:
                            playerOneAtoms.append(tuple([row, column]))
                            # Set that location to one
                            grid[row][column] += 1
                            turn = turn + 1
                            checkForRowAndColumn(row, column, 1)
                            # print("Click ", pos, "Grid coordinates: ", row, column)
                            print("thisPlayerAtoms are: ", playerOneAtoms)
                            print("otherPlayerAtoms are: ", playerTwoAtoms)

                #processing grid data
                grid_data=recv_data[3]
                flag=1
                if not self.check_grid(grid_data, playerOneAtoms, playerTwoAtoms):
                    flag=0
                
                #add the function to cross check grid here 
                if recv_data[3] == grid:
                    print("It is correct")
                else:
                    print("It is incorrect")

                # player2.send(recvdata)
                #recvdata = player2.recv(1024)
                #if pickle.loads(recvdata) ==1:
            else:

                signal_and_data = []
                signal_and_data.append(0)
                signal_and_data.append(playerOneAtoms)
                player1.send(pickle.dumps(signal_and_data))
                signal_and_data[0] = 1
                player2.send(pickle.dumps(signal_and_data))
                recvdata = player2.recv(1024)
                recv_data=pickle.loads(recvdata)
                #After we've recieved the data first we will need to compute everything and make changes to our grid locally
                if recv_data[0] == 1:
                    #this the quit command, this client has exited the game
                    print("This player wants to quit the game")
                if recv_data[0] == 2:
                    #This is the mousebutton command

                    column = recv_data[5] // (WIDTH + MARGIN)
                    row = recv_data[4] // (HEIGHT + MARGIN)

                    if (row, column) in playerOneAtoms:
                        print("You can't click there")
                    else:
                        if (row, column) in playerTwoAtoms:
                            print("It is already in the block")  
                            # Set that location to one
                            grid[row][column] += 1
                            turn = turn + 1
                            checkForRowAndColumn(row, column, 2)
                            # print("Click ", pos, "Grid coordinates: ", row, column)
                            print("thisPlayerAtoms are: ", playerOneAtoms)
                            print("otherPlayerAtoms are: ", playerTwoAtoms)

                        else:
                            playerTwoAtoms.append(tuple([row, column]))
                            # Set that location to one
                            grid[row][column] += 1
                            turn = turn + 1
                            checkForRowAndColumn(row, column, 2)
                            # print("Click ", pos, "Grid coordinates: ", row, column)
                            print("thisPlayerAtoms are: ", playerOneAtoms)
                            print("otherPlayerAtoms are: ", playerTwoAtoms)

                #processing grid data
                grid_data=recv_data[3]
                flag=1
                if not self.check_grid(grid_data, playerOneAtoms, playerTwoAtoms):
                    flag=0
                
                #add the function to cross check grid here 
                if recv_data[3] == grid:
                    print("It is correct")
                else:
                    print("It is incorrect")
                # player2.send(recvdata)
                #recvdata = player2.recv(1024)
                #if pickle.loads(recvdata) ==1:
















    
    #def cross_check_data()




room=Thread(target=room_creator, args=())
room.start()

    




server = socket(AF_INET, SOCK_STREAM)
server.bind((LOCALHOST, server_port))
server.listen(50)

while True:
    
    connection, client_address = server.accept()
    connstream = ssl.wrap_socket(connection,server_side=True,certfile="server.crt", keyfile="server.key")
    try:
        sentence = connstream.recv(1024)
        
        if sentence:
            data=pickle.loads(sentence)
            if namereg.match(data[0]) is None:
                data=-1

            elif data[0] not in userlist:

                ipand=[]
                ipand.append(data[1])
                ipand.append(data[2])
                

                if ports > 64000:
                    ports=60000
                while ports in occupied_ports:
                    ports=ports+1    
                
                occupied_ports.append(ports)
                ipand.append(ports)
                ipand.append(1)
                userlist[data[0]]=ipand
                
                currport=ports
                currname=data[0]
                ports=ports+1
            
            else:
                data=-1
        
        print("Recieved = "+client_address[0]+" : "+str(client_address[1]))
        #data="dad"
        sentence=pickle.dumps(currport)
        connstream.send(sentence)
        #connstream.shutdown(SHUT_RDWR)
        connstream.close()
        #connection.close()
        if data != -1:

            t=Thread(target=client_specific_server, args=(currport,currname,))
            t.start()
    except:
        print("Error")
        sys.exit(0)
        