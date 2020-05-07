import pickle
import re
from socket import *
import sys
import ssl
import pprint
import pygame
from tkinter import *   

# Define some colors
LIGHT_RED = (249, 200, 200)
LIGHT_GREEN = (200, 249, 226)
LIGHT_RED_2 = (243, 95, 129)
LIGHT_GREEN_2 = (101, 255, 78)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (88, 214, 141)
RED = (231, 76, 60)
DARK_GREEN = (12, 75, 3)
DARK_RED = (124, 13, 43)
ORANGE = (255,174,66)
YELLOW = (255,255,0)

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 40
HEIGHT = 40
 
# This sets the margin between each cell
MARGIN = 5

grid = []
for row in range(10):
    # Add an empty array that will hold each cell
    # in this row
    grid.append([])
    for column in range(10):
        grid[row].append(0)  # Append a cell


# a is just an example of grid
a=[[0]*6 for i in range(11)]
b=[]
#regex is our regular expression for input validation of username
regex=re.compile("^[a-zA-Z0-9]{0,20}$")

#We ask user for input and check if it satisfies regex
username=input("Give username : ")
while regex.match(username) is None:
    username=input("Invalid input, please Re-Enter username : ")

#Adding username, machine's ipaddress and the machine's name to a variable  b to send to server
b.append(username)
b.append(gethostbyname(gethostname()))
b.append(gethostname())

#convert the list "b" into a byte format using pickle and store it in a variable named "data"
data=pickle.dumps(b)

#Creating a socket and setting the socket timeout as 10 seconds 
serverName = '127.0.0.1'
serverPort = 49999
clientSocket = socket(AF_INET, SOCK_STREAM)
#clientSocket.bind(("127.0.0.1", 40000))
clientSocket.settimeout(10)

#Using ssl with socket
try:
    ssl_sock = ssl.wrap_socket(clientSocket,ca_certs="server.crt",cert_reqs=ssl.CERT_REQUIRED)
except:
    print("SSL error in wrap sockets")
    sys.exit(0)

#Creating a connection with server
try:
    ssl_sock.connect((serverName,serverPort))
except:
    print("Connection Error")
    sys.exit(0)

######Printing SSL data like, server's machine name , type of cyphers in use, SSL certificate 
print (repr(ssl_sock.getpeername()))
print (ssl_sock.cipher())
print (pprint.pformat(ssl_sock.getpeercert()))
######Printing SSL (It is not really important, it's for the sake of debugging)

# send the byte data in "data" variable to server, recieve the response from server, convert the from server from byte to normal format
try:
    ssl_sock.send(data)
    modifieddata = ssl_sock.recv(1024)
    data=pickle.loads(modifieddata) 
    #this "data" variable stores the port number specifically assigned to the user eg. 65000 and if there is an error
    #or the username is  already present in backend, we return -1
    print(data)
    ssl_sock.close()
except:
    print("Error in sending or receiving data")
    sys.exit(0)

#username is already present 
if data == -1:
    print("Name is already there in buffer")
    sys.exit(0)

#Create a new client socket to create a connection with server on the server given port
clientSocket = socket(AF_INET, SOCK_STREAM)
try:
    ssl_sock = ssl.wrap_socket(clientSocket,ca_certs="server.crt",cert_reqs=ssl.CERT_REQUIRED)
except:
    print("SSL error in wrap sockets")
    sys.exit(0)

try:
    ssl_sock.connect((serverName,int(data)))
except:
    print("Connection error")
    sys.exit(0)

#Sending some data to server (To tell server the new client connection is ready)
data=pickle.dumps(1)
ssl_sock.send(data)
#Receive the data sent by the server (To tell the client the new connection at server side is also ready)
# "modifieddata" stores this string " You are added in buffer"
modifieddata = ssl_sock.recv(1024)
data=pickle.loads(modifieddata) 
print(data)

#This loop is used to wait for room creation
# Atleast two users should be connected to server to start a game
#Every 5 seconds, the servers check for number of connections, if there is only one user, the server sends "Waiting"
#If server has found a another player, server sends "Ready"
while data != "Ready":
    modifieddata = ssl_sock.recv(1024)
    data=pickle.loads(modifieddata)
    print(data) 

# server sends the other players's name
modifieddata = ssl_sock.recv(1024)
data=pickle.loads(modifieddata)
print("Your opponentis : "+ str(data)) 

#After the connection is established, The game window will start
#First thing we need to do is assign turns to the player
#Declaring two variables for the atoms
thisPlayerAtoms = []
otherPlayerAtoms = []

done = False

# Initialize pygame
pygame.init()
 
# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [400, 400]
screen = pygame.display.set_mode(WINDOW_SIZE)

# Set title of screen
pygame.display.set_caption("Game Window:")
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()


def sendDatatoServer(typeOfEvent, thisPlayerAtoms, otherPlayerAtoms, grid, row, column):
    my_data = []
    my_data.append(typeOfEvent)
    my_data.append(thisPlayerAtoms)
    my_data.append(otherPlayerAtoms)
    my_data.append(grid)
    my_data.append(row)
    my_data.append(column)
    # data = pickle.dumps(data_to_be_sent_in_whatever_format)
<<<<<<< HEAD
    # ssl_sock.send(data)
    mydata={}
    mydata["event"]=typeOfEvent
    mydata["playone"]=typeOfEvent
    
    ssl_sock.send(pickle.dumps(mydata))


=======
    ssl_sock.send(pickle.dumps(my_data))
>>>>>>> bc1f897529aac0eb568d04936304a85f4bf7df34


#Gaming algorithm
def deleteTheAtom(row, column):
    if (row, column) in thisPlayerAtoms:
        thisPlayerAtoms.remove(tuple([row, column]))
    if (row, column) in otherPlayerAtoms:
        otherPlayerAtoms.remove(tuple([row, column]))


def checkForRowAndColumn(row, column, player_turn):
    if (row == 0 and column == 0):
        #We have to burst at two
        if(grid[row][column] == 2):
            grid[row][column] = 0
            grid[row+1][column] += 1
            deleteTheAtom(row+1, column)
            if player_turn == 1:
                thisPlayerAtoms.append(tuple([row+1, column]))
            elif player_turn == 2:
                otherPlayerAtoms.append(tuple([row+1, column]))
            checkForRowAndColumn(row+1, column, player_turn)
            grid[row][column+1] += 1
            deleteTheAtom(row, column+1)
            if player_turn == 1:
                thisPlayerAtoms.append(tuple([row, column+1]))
            elif player_turn == 2:
                otherPlayerAtoms.append(tuple([row, column+1]))
            checkForRowAndColumn(row, column+1, player_turn)

    if (row == 9 and column == 0):
        #We have to burst at two
        if(grid[row][column] == 2):
            grid[row][column] = 0
            grid[row-1][column] += 1
            deleteTheAtom(row-1, column)
            if player_turn == 1:
                thisPlayerAtoms.append(tuple([row-1, column]))
            elif player_turn == 2:
                otherPlayerAtoms.append(tuple([row-1, column]))
            checkForRowAndColumn(row-1, column, player_turn)
            grid[row][column+1] += 1
            deleteTheAtom(row, column+1)
            if player_turn == 1:
                thisPlayerAtoms.append(tuple([row, column+1]))
            elif player_turn == 2:
                otherPlayerAtoms.append(tuple([row+1, column+1]))
            checkForRowAndColumn(row, column+1, player_turn)

    if (row == 0 and column == 9):
        if(grid[row][column] == 2):
            grid[row][column] = 0
            grid[row+1][column] += 1
            deleteTheAtom(row+1, column)
            if player_turn == 1:
                thisPlayerAtoms.append(tuple([row+1, column]))
            elif player_turn == 2:
                otherPlayerAtoms.append(tuple([row+1, column]))
            checkForRowAndColumn(row+1, column, player_turn)
            grid[row][column-1] += 1
            deleteTheAtom(row, column-1)
            if player_turn == 1:
                thisPlayerAtoms.append(tuple([row, column-1]))
            elif player_turn == 2:
                otherPlayerAtoms.append(tuple([row+1, column-1]))
            checkForRowAndColumn(row, column-1, player_turn)


    if (row == 9 and column == 9):
        if(grid[row][column] == 2):
            grid[row][column] = 0
            grid[row-1][column] += 1
            deleteTheAtom(row-1, column)
            if player_turn == 1:
                thisPlayerAtoms.append(tuple([row-1, column]))
            elif player_turn == 2:
                otherPlayerAtoms.append(tuple([row-1, column]))
            checkForRowAndColumn(row-1, column, player_turn)
            grid[row][column-1] += 1
            deleteTheAtom(row, column-1)
            if player_turn == 1:
                thisPlayerAtoms.append(tuple([row, column-1]))
            elif player_turn == 2:
                otherPlayerAtoms.append(tuple([row, column-1]))
            checkForRowAndColumn(row, column-1, player_turn)

    if (row == 0 and column >=1 and column <=8):
        #We now check for three
        if(grid[row][column] == 3):
            grid[row][column] = 0
            grid[row+1][column] += 1
            deleteTheAtom(row+1, column)
            if player_turn == 1:
                thisPlayerAtoms.append(tuple([row+1, column]))
            elif player_turn == 2:
                otherPlayerAtoms.append(tuple([row+1, column]))
            checkForRowAndColumn(row+1, column, player_turn)
            grid[row][column+1] += 1
            deleteTheAtom(row, column+1)
            if player_turn == 1:
                thisPlayerAtoms.append(tuple([row, column+1]))
            elif player_turn == 2:
                otherPlayerAtoms.append(tuple([row, column+1]))
            checkForRowAndColumn(row, column+1, player_turn)
            grid[row][column-1] += 1
            deleteTheAtom(row, column-1)
            if player_turn == 1:
                thisPlayerAtoms.append(tuple([row, column-1]))
            elif player_turn == 2:
                otherPlayerAtoms.append(tuple([row, column-1]))
            checkForRowAndColumn(row, column-1, player_turn)

    if (row == 9 and column >=1 and column <=8):
        if(grid[row][column] == 3):
            grid[row][column] = 0
            grid[row-1][column] += 1
            deleteTheAtom(row-1, column)
            if player_turn == 1:
                thisPlayerAtoms.append(tuple([row-1, column]))
            elif player_turn == 2:
                otherPlayerAtoms.append(tuple([row-1, column]))
            checkForRowAndColumn(row-1, column, player_turn)
            grid[row][column+1] += 1
            deleteTheAtom(row, column+1)
            if player_turn == 1:
                thisPlayerAtoms.append(tuple([row, column+1]))
            elif player_turn == 2:
                otherPlayerAtoms.append(tuple([row, column+1]))
            checkForRowAndColumn(row, column+1, player_turn)
            grid[row][column-1] += 1
            deleteTheAtom(row, column-1)
            if player_turn == 1:
                thisPlayerAtoms.append(tuple([row, column-1]))
            elif player_turn == 2:
                otherPlayerAtoms.append(tuple([row, column-1]))
            checkForRowAndColumn(row, column-1, player_turn)

    if (column == 9 and row >=1 and row <=8):
        if(grid[row][column] == 3):
            grid[row][column] = 0
            grid[row-1][column] += 1
            deleteTheAtom(row-1, column)
            if player_turn == 1:
                thisPlayerAtoms.append(tuple([row-1, column]))
            elif player_turn == 2:
                otherPlayerAtoms.append(tuple([row-1, column]))
            checkForRowAndColumn(row-1, column, player_turn)
            grid[row+1][column] += 1
            deleteTheAtom(row+1, column)
            if player_turn == 1:
                thisPlayerAtoms.append(tuple([row+1, column]))
            elif player_turn == 2:
                otherPlayerAtoms.append(tuple([row+1, column]))
            checkForRowAndColumn(row+1, column, player_turn)
            grid[row][column-1] += 1
            deleteTheAtom(row, column-1)
            if player_turn == 1:
                thisPlayerAtoms.append(tuple([row, column-1]))
            elif player_turn == 2:
                otherPlayerAtoms.append(tuple([row, column-1]))
            checkForRowAndColumn(row, column-1, player_turn)


    if (column == 0 and row >=1 and row <=8):
        if(grid[row][column] == 3):
            grid[row][column] = 0
            grid[row-1][column] += 1
            deleteTheAtom(row-1, column)
            if player_turn == 1:
                thisPlayerAtoms.append(tuple([row-1, column]))
            elif player_turn == 2:
                otherPlayerAtoms.append(tuple([row-1, column]))
            checkForRowAndColumn(row-1, column, player_turn)
            grid[row+1][column] += 1
            deleteTheAtom(row+1, column)
            if player_turn == 1:
                thisPlayerAtoms.append(tuple([row+1, column]))
            elif player_turn == 2:
                otherPlayerAtoms.append(tuple([row+1, column]))
            checkForRowAndColumn(row+1, column, player_turn)
            grid[row][column+1] += 1
            deleteTheAtom(row, column+1)
            if player_turn == 1:
                thisPlayerAtoms.append(tuple([row, column+1]))
            elif player_turn == 2:
                otherPlayerAtoms.append(tuple([row, column+1]))
            checkForRowAndColumn(row, column+1, player_turn)

    else:
        checkForTheFour(row, column, player_turn)

done = False

def checkForWin():
    if(len(thisPlayerAtoms) == 0):
        #Player 2 has won, end the game
        print("Player 2 won")
        done = True
    elif(len(otherPlayerAtoms) == 0):
        #Player 1 has won, end the game
        print("Player 1 won")
        done = True
    else:
        #Game is still going on, continue
        return  


def checkForTheFour(row, column, player_turn):
    if(grid[row][column] == 4):
        grid[row][column] = 0
        grid[row+1][column] += 1
        deleteTheAtom(row+1, column)
        if player_turn == 1:
            thisPlayerAtoms.append(tuple([row+1, column]))
        elif player_turn == 2:
            otherPlayerAtoms.append(tuple([row+1, column]))
        checkForRowAndColumn(row+1, column, player_turn)
        grid[row][column+1] += 1
        deleteTheAtom(row, column+1)
        if player_turn == 1:
            thisPlayerAtoms.append(tuple([row, column+1]))
        elif player_turn == 2:
            otherPlayerAtoms.append(tuple([row, column+1]))
        checkForRowAndColumn(row, column+1, player_turn)
        grid[row-1][column] += 1
        deleteTheAtom(row-1, column)
        if player_turn == 1:
            thisPlayerAtoms.append(tuple([row-1, column]))
        elif player_turn == 2:
            otherPlayerAtoms.append(tuple([row-1, column]))  
        checkForTheFour(row-1, column, player_turn)
        grid[row][column-1] += 1
        deleteTheAtom(row, column-1)
        if player_turn == 1:
            thisPlayerAtoms.append(tuple([row, column-1]))
        elif player_turn == 2:
            otherPlayerAtoms.append(tuple([row, column-1]))
        checkForRowAndColumn(row, column-1, player_turn)


screen.fill(GREEN)
for row in range(10):
        for column in range(10):
            color = WHITE

            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])

while not done:
    event = 0
    signal_move = 0
    data_for_move = ssl_sock.recv(1024)
    signal_move_prime = pickle.loads(data_for_move)
    # signal_move = signal_move_prime["signal"]
    print("Signal recieved from Server", signal_move_prime)
    # print(type(signal_move_prime))
    if signal_move_prime[0] == 1:
        otherPlayerAtoms = signal_move_prime[1]
        #Now, we know that it's our turn
        for event in pygame.event.get():
            #Now we've got event of this client
            if event.type == pygame.QUIT:  # If user clicked close
                event = 1
                done = True  # Flag that we are done so we exit this loop
                #Now we need to send a signal to server saying that this player has quit the game
            elif event.type == pygame.MOUSEBUTTONDOWN:
                event = 2
            # User clicks the mouse. Get the position
                pos = pygame.mouse.get_pos()
                # Change the x/y screen coordinates to grid coordinates
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)

                if (row, column) in otherPlayerAtoms:
                    print("You can't click there")
                else:
                    if (row, column) in thisPlayerAtoms:
                        print("It is already in the block")   
                        # Set that location to one
                        grid[row][column] += 1
                        turn = turn + 1
                        checkForRowAndColumn(row, column, 1)
                        print("Click ", pos, "Grid coordinates: ", row, column)
                        print("thisPlayerAtoms are: ", thisPlayerAtoms)
                        print("otherPlayerAtoms are: ", otherPlayerAtoms)
                    else:
                        otherPlayerAtoms.append(tuple([row, column]))
                        # Set that location to one
                        grid[row][column] += 1
                        turn = turn + 1
                        checkForRowAndColumn(row, column, 1)
                        print("Click ", pos, "Grid coordinates: ", row, column)
                        print("thisPlayerAtoms are: ", thisPlayerAtoms)
                        print("otherPlayerAtoms are: ", otherPlayerAtoms)

        #This is where I have to send the data
        sendDatatoServer(event, thisPlayerAtoms, otherPlayerAtoms, grid, row, column)


    #Now Drawing it on the screen
    for row in range(10):
        for column in range(10):
            color = WHITE
            # if grid[row][column] == 1:
            #     if (turn % 2):
            #         color = LIGHT_RED
            #     else:
            #         color = LIGHT_GREEN
            # if grid[row][column] == 2:
            #     if (turn % 2):
            #         color = LIGHT_RED_2
            #     else:
            #         color = LIGHT_GREEN_2
            # if grid[row][column] == 3:
            #     if (turn % 2):
            #         color = RED
            #     else:
            #         color = GREEN
            # if grid[row][column] == 4:
            #     if (turn % 2):
            #         color = DARK_RED
            #     else:
            #         color = DARK_GREEN
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])

    #This is to update the screen according to player one
    for row in range(10):
        for column in range(10):
            #Color of the player one is green
            if (row, column) in thisPlayerAtoms:
                if grid[row][column] == 1:
                    color = LIGHT_GREEN
                elif grid[row][column] == 2:
                    color = LIGHT_GREEN_2
                elif grid[row][column] == 3:
                    color = GREEN
                else:
                    color = DARK_GREEN
                pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])

    #This is to update the screen according to player two
    for row in range(10):
        for column in range(10):
            #Color of the player one is red
            if (row, column) in otherPlayerAtoms:
                if grid[row][column] == 1:
                    color = LIGHT_RED
                elif grid[row][column] == 2:
                    color = LIGHT_RED_2
                elif grid[row][column] == 3:
                    color = RED
                else:
                    color = DARK_RED
                pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])

    # screen.fill(RED)
 
    # Limit to 60 frames per second
    clock.tick(60)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

#Use these functions to send or recieve data
#send
# data = pickle.dumps(data_to_be_sent_in_whatever_format)
# ssl_sock.send(data)
# receive
# data_from_server = ssl_sock.recv(1024)
# data = pickle.loads (data_from_server)


ssl_sock.close()


    #name=gethostbyname(gethostname())
    #print(name)
    #print(gethostname())
#except :
#	print("Connection error")
	