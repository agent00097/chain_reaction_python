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

  

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 40
HEIGHT = 40
 
# This sets the margin between each cell
MARGIN = 5

#defining turn
#turn = 1

done = False
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
    
    playerOneAtoms = []
    playerTwoAtoms = []
    grid = [[0]*10]*10
    

    def __init__(self, play1, play2):
        Thread.__init__(self)
        self.play1=play1
        self.play2=play2

    def deleteTheAtom(self, row, column):
        if (row, column) in self.playerOneAtoms:
            self.playerOneAtoms.remove(tuple([row, column]))
        if (row, column) in self.playerTwoAtoms:
            self.playerTwoAtoms.remove(tuple([row, column]))


    def checkForRowAndColumn(self, row, column, player_turn):
        if (row == 0 and column == 0):
            #We have to burst at two
            if(self.grid[row][column] == 2):
                self.grid[row][column] = 0
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

        if (row == 9 and column == 0):
            #We have to burst at two
            if(self.grid[row][column] == 2):
                self.grid[row][column] = 0
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

        if (row == 0 and column == 9):
            if(self.grid[row][column] == 2):
                self.grid[row][column] = 0
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


        if (row == 9 and column == 9):
            if(self.grid[row][column] == 2):
                self.grid[row][column] = 0
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

        if (row == 0 and column >=1 and column <=8):
            #We now check for three
            if(self.grid[row][column] == 3):
                self.grid[row][column] = 0
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

        if (row == 9 and column >=1 and column <=8):
            if(self.grid[row][column] == 3):
                self.grid[row][column] = 0
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

        if (column == 9 and row >=1 and row <=8):
            if(self.grid[row][column] == 3):
                self.grid[row][column] = 0
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


        if (column == 0 and row >=1 and row <=8):
            if(self.grid[row][column] == 3):
                self.grid[row][column] = 0
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

    
    def checkForWin(self):
        if(len(self.playerOneAtoms) == 0):
            print("Player 2 won")
        elif(len(self.playerTwoAtoms) == 0):
            print("Player 1 won")
        else:
            return  


    def checkForTheFour(self,row, column, player_turn):
        if(self.grid[row][column] == 4):
            self.grid[row][column] = 0
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

        turn=1
        while True:
            print("This executes\n")
            if turn%2 == 1:
                #New dictionary
                signal_and_data = []
                signal_and_data.append(0)
                signal_and_data.append(self.playerTwoAtoms)
                player2.send(pickle.dumps(signal_and_data))
                signal_and_data[0] = 1
                player1.send(pickle.dumps(signal_and_data))
                print("Data sent to player 1\n")

                recvdata = player1.recv(1024)
                recv_data=pickle.loads(recvdata)
                print("Data recieved by Player 1\n")
                print(recv_data)

                #After we've recieved the data first we will need to compute everything and make changes to our grid locally
                if recv_data[0] == 1:
                    print("DEBUG: player 1 clicked on the exit button")
                    #this the quit command, this client has exited the game
                    print("This player wants to quit the game")
                if recv_data[0] == 2:
                    #This is the mousebutton command

                    print("DEBUG: Player 1 click on one of the cell")

                    column = recv_data[5]
                    row = recv_data[4]
                    
                    print("DEBUG: row ",row," and column ", column, "were obtained")

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
                turn=turn+1
                grid_data=recv_data[3]
                flag=1
                if not self.check_grid(grid_data, recv_data[1], recv_data[2]):
                    flag=0
                
                #add the function to cross check grid here 
                if recv_data[3] == self.grid:
                    print("It is correct")
                else:
                    print("It is incorrect")
                    flag=0
                

                #player1.send(pickle.dumps(flag))
                # player1.send(pickle.dumps(1))
                #recvdata = player2.recv(1024)
                #if pickle.loads(recvdata) ==1:
            else:

                #New dictionary
                signal_and_data = []
                signal_and_data.append(0)
                signal_and_data.append(self.playerOneAtoms)
                player1.send(pickle.dumps(signal_and_data))
                signal_and_data[0] = 1
                player2.send(pickle.dumps(signal_and_data))
                print("Data sent to player 2\n")

                recvdata = player2.recv(1024)
                recv_data=pickle.loads(recvdata)
                print("Data recieved by Player 2\n")
                print(recv_data)
                
                

                
                #After we've recieved the data first we will need to compute everything and make changes to our grid locally
                if recv_data[0] == 1:
                    #this the quit command, this client has exited the game
                    print("This player wants to quit the game")
                if recv_data[0] == 2:
                    #This is the mousebutton command

                    print("DEBUG: Inside Player 2:  Player 2 has clicked on a cell")

                    column = recv_data[5]
                    row = recv_data[4]

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
                turn=turn+1
                grid_data=recv_data[3]
                flag=1
                if not self.check_grid(grid_data, recv_data[1], recv_data[2]):
                    flag=0
                
                #add the function to cross check grid here 
                if recv_data[3] == self.grid:
                    print("It is correct")
                else:
                    print("It is incorrect")
                    flag=0
                #player2.send(pickle.dumps(flag))
                # player2.send(pickle.dumps(1))
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
        