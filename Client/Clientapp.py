import pickle
import re
from socket import *
import sys
import ssl
import pprint
import pygame
from tkinter import * 
from tkinter import messagebox 

# Define some colors
LIGHT_RED = (255, 180, 180)
LIGHT_GREEN = (200, 249, 226)
LIGHT_RED_2 = (247, 109, 109)
LIGHT_GREEN_2 = (101, 255, 78)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (88, 214, 141)
RED = (242, 47, 47)
DARK_GREEN = (12, 75, 3)
DARK_RED = (179, 21, 21)
ORANGE = (255,174,66)
YELLOW = (255,255,0)

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 40
HEIGHT = 40
 
# This sets the margin between each cell
MARGIN = 5

grid = [[0]*10]*10
grid = [ ([0] * 10) for row in range(10)]


# myfont = pygame.font.SysFont("monospace", 15)

# a is just an example of grid
a=[[0]*6 for i in range(11)]
b=[]
#regex is our regular expression for input validation of username
regex=re.compile("^[a-zA-Z0-9]{0,20}$")
regpass=re.compile("^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$")

#We ask user for input and check if it satisfies regex
# userin=input("Press 1 to Log on , press to 2 login : ")
# if int(userin) == 1: 
#     print(userin)
#     logon_or_login="logon"
#     username=input("Give username : ")
#     print("Enter Logon Credentials")
#     while regex.match(username) is None:
#         username=input("Invalid input, please Re-Enter username : ")

#     passw=input("Give password : ")
#     repassw=input("Re-enter password : ")
#     while regpass.match(passw) is None or passw!=repassw:
#         passw=input("Give password : ")
#         repassw=input("Re-enter password : ")
# else:
#     logon_or_login="login"
#     print("Enter Login Credentials")
#     username=input("Give username : ")
#     while regex.match(username) is None:
#         username=input("Invalid input, please Re-Enter username : ")

#     passw=input("Give password : ")
#     while regpass.match(passw) is None:
#         passw=input("Give password : ")
        


data=""

#Adding username, machine's ipaddress and the machine's name to a variable  b to send to server
def connect_and_check_server(params):
    global data
    (loginlogon,usern,pasw) = params
    b.append(loginlogon)
    b.append(usern)
    b.append(pasw)
    b.append(gethostbyname(gethostname()))
    b.append(gethostname())

    #convert the list "b" into a byte format using pickle and store it in a variable named "data"
    data_temp=pickle.dumps(b)

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
        print("Connection Error in first one")
        sys.exit(0)

    ######Printing SSL data like, server's machine name , type of cyphers in use, SSL certificate 
    print (repr(ssl_sock.getpeername()))
    print (ssl_sock.cipher())
    print (pprint.pformat(ssl_sock.getpeercert()))
    ######Printing SSL (It is not really important, it's for the sake of debugging)


    try:
        ssl_sock.send(data_temp)
        modifieddata = ssl_sock.recv(1024)
        data_temp=pickle.loads(modifieddata) 
        
        print(data_temp)
        ssl_sock.close()
    except:
        print("Error in sending or receiving data")
        sys.exit(0)

    #username is already present 
    if data_temp == -1:
        print("Name is already there in database")
        alert_popup("Error...", "Name is already there in database",helloCallBack)
    elif data_temp == -2:
        print("Username or password or data sent is in incorrect format")
        alert_popup("Error...", "Username or password or data sent is in incorrect format",helloCallBack)
    elif data_temp== -3:
        print("Username is not there in database")
        alert_popup("Error...", "Username is not there in database",helloCallBack)
    elif data_temp== -4:
        print("Password is incorect")
        alert_popup("Error...", "Password is incorect",helloCallBack)
    else:
        print("You are connected successfully ")
        alert_popup("Being connected...", "Game starts....",root.destroy)
        print(data_temp)
    data=data_temp
    return data_temp
#######################################################


def connect_server_2():
    global username,passw,logon_or_login
    username = v.get() 
    passw = t.get() 
    alert_popup("Wait","You have been added to buffer ... ",connect_and_check_server,("logon",username,passw))

def connect_server_1():
    global username,passw,logon_or_login
    username = v.get() 
    passw = t.get()
    alert_popup("Wait","You have been added to buffer ... ",connect_and_check_server,("login",username,passw))
def helloCallBack():
    
    test=root.pack_slaves()
    for i in test:
        i.pack_forget()

    def regChecker_1():
        username=v.get()
        password=t.get()
        if not(regex.match(username) or regex.match(password)):
            alert_popup("Chain reaction...","Regex not matched",helloCallBack)
        else:
            connect_server_1()
    def regChecker_2():
        username=v.get()
        password=t.get()
        if not(regex.match(username) or regex.match(password)):
            alert_popup("Chain reaction...","Regex not matched",helloCallBack)
        else:
            connect_server_2()
    

    def login():
        # alert_popup("Test1","Player Name : "+str(v.get())+"\nClick ok to start the game",connect_server)
        test=root.pack_slaves()
        for i in test:
            i.pack_forget()

        
        l=Label(root, text="""Enter Username and Password""",justify = "left",padx = 20)
        l.pack(side= "top")

        a = Label(root, text="Username",justify = "left")
        b = Label(root, text="Password",justify = "left",padx = 10, )

        a.pack(side = "left")

        t.pack(side = "right")
        b.pack(side = "left")

        v.pack(side = "right")
        Button(root, text="Log In", command=regChecker_1 , width=200).pack(side = "bottom")

    def logon():
        # alert_popup("Test1","Player Name : "+str(v.get())+"\nClick ok to start the game",connect_server)
        test=root.pack_slaves()
        for i in test:
            i.pack_forget()
        l=Label(root, text="""Enter username and Password""",justify ="left",padx = 20)
        l.pack(side= "top")

        a = Label(root, text="Username",justify = "left")
        b = Label(root, text="Password",justify = "left",padx = 10, )

        a.pack(side = "left")

        t.pack(side = "right")
        b.pack(side = "left")

        v.pack(side = "right")

        Button(root, text="Sign Up", command=regChecker_2 , width=200).pack(side = "bottom")
    
    Button(root, text="Sign Up", command=logon , width=200).pack()
    Button(root, text="Sign In", command=login , width=200).pack(side ="bottom")
def alert_popup(title, message,func,params=None):
   
    """Generate a pop-up window for special messages."""
    test=root.pack_slaves()
    for i in test:
        i.pack_forget()
    root.title(title)
    m = message
    m += '\n'
    w = Label(root, text=message, width=120, height=10)
    w.pack()
    if (params!=None):
        b = Button(root, text="OK", command=func(params) , width=10)
        b.config(width=200, height=200)

    else:
        b = Button(root, text="OK", command=func , width=10)
        b.config(width=200, height=200)

    b.pack()

#modified
root=Tk()

v=Entry(root,justify = RIGHT)
t=Entry(root,justify=RIGHT)
w = 500     # popup window width
h = 200     # popup window height
sw = root.winfo_screenwidth()
sh = root.winfo_screenheight()
x = (sw - w)/2
y = (sh - h)/2
root.geometry('%dx%d+%d+%d' % (w, h, x, y))
alert_popup("Chain Reaction...", "Connecting to server",helloCallBack)

root.mainloop()

print("Username is " +username)

#######################
# data=connect_and_check_server(logon_or_login,username,passw)

#Create a new client socket to create a connection with server on the server given port
clientSocket = socket(AF_INET, SOCK_STREAM)
try:
    ssl_sock = ssl.wrap_socket(clientSocket,ca_certs="server.crt",cert_reqs=ssl.CERT_REQUIRED)
except:
    print("SSL error in wrap sockets")
    sys.exit(0)

try:
    ssl_sock.connect(("127.0.0.1",int(data)))
except:
    print("Connection error 11")
    sys.exit(0)

pygame.init()

font = pygame.font.Font('freesansbold.ttf', 32) 
 
# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [400, 400]
screen = pygame.display.set_mode(WINDOW_SIZE)

# Set title of screen
pygame.display.set_caption("Choose Option:")
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

#Sending some data to server (To tell server the new client connection is ready)
data=pickle.dumps(1)
ssl_sock.send(data)
modifieddata = ssl_sock.recv(4096)
data=pickle.loads(modifieddata) 
for ax in data:
    print(ax)

win_here = data[0]
loss_here = data[1]
moves = ax


modifieddata = ssl_sock.recv(1024)
data=pickle.loads(modifieddata)
print(data)

root=Tk()

v=Entry(root,justify = RIGHT)
t=Entry(root,justify=RIGHT)
w = 500     # popup window width
h = 200     # popup window height
sw = root.winfo_screenwidth()
sh = root.winfo_screenheight()
x = (sw - w)/2
y = (sh - h)/2
stats="Wins - "+str(win_here)+ "\nLost - " +str(loss_here) + "\nMoves - "+str(ax)
root.geometry('%dx%d+%d+%d' % (w, h, x, y))
alert_popup("Your Statistics", stats, root.destroy)

root.mainloop()
x=ax


while data != "Ready":
    modifieddata = ssl_sock.recv(1024)
    data=pickle.loads(modifieddata)
    print(data) 

# server sends the other players's name
modifieddata = ssl_sock.recv(1024)
data=pickle.loads(modifieddata)
print("Your opponent is : "+ str(data)) 

#After the connection is established, The game window will start
#First thing we need to do is assign turns to the player
#Declaring two variables for the atoms
thisPlayerAtoms = []
otherPlayerAtoms = []

done = False



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


def sendDatatoServer(typeOfEvent, tPlayerAtoms, oPlayerAtoms, grid, row, column):
    my_data = []
    my_data.append(typeOfEvent)
    my_data.append(tPlayerAtoms)
    my_data.append(oPlayerAtoms)
    my_data.append(grid)
    my_data.append(row)
    my_data.append(column)
    print(my_data)
    data = pickle.dumps(my_data)
    # ssl_sock.send(data)
    ssl_sock.send(data)




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
            deleteTheAtom(row,column)
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

    if (row == 8 and column == 0):
        #We have to burst at two
        if(grid[row][column] == 2):
            grid[row][column] = 0
            deleteTheAtom(row,column)
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

    if (row == 0 and column == 8):
        if(grid[row][column] == 2):
            grid[row][column] = 0
            deleteTheAtom(row,column)
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


    if (row == 8 and column == 8):
        if(grid[row][column] == 2):
            grid[row][column] = 0
            deleteTheAtom(row,column)
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

    if (row == 0 and column >=1 and column <=7):
        #We now check for three
        if(grid[row][column] == 3):
            grid[row][column] = 0
            deleteTheAtom(row,column)
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

    if (row == 8 and column >=1 and column <=7):
        if(grid[row][column] == 3):
            grid[row][column] = 0
            deleteTheAtom(row,column)
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

    if (column == 8 and row >=1 and row <=7):
        if(grid[row][column] == 3):
            grid[row][column] = 0
            deleteTheAtom(row,column)
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


    if (column == 0 and row >=1 and row <=7):
        if(grid[row][column] == 3):
            grid[row][column] = 0
            deleteTheAtom(row,column)
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
        deleteTheAtom(row,column)
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




data_for_first = ssl_sock.recv(1024)
first_data = pickle.loads(data_for_first)
print("First="+first_data)

def screenUpdate():

    for row in range(10):
            for column in range(10):
                color = BLACK

                pygame.draw.rect(screen,
                                color,
                                [(MARGIN + WIDTH) * column + MARGIN,
                                (MARGIN + HEIGHT) * row + MARGIN,
                                WIDTH,
                                HEIGHT])

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
                    elif grid[row][column] == 4:
                        color = DARK_GREEN
                    pygame.draw.rect(screen,
                                color,
                                [(MARGIN + WIDTH) * column + MARGIN,
                                (MARGIN + HEIGHT) * row + MARGIN,
                                WIDTH,
                                HEIGHT])


    # print("DEBUG: Just filled in all the cells according to this client")

        #This is to update the screen according to player two
    for row in range(10):
        for column in range(10):
                #Color of the player one is red
            if (row, column) in otherPlayerAtoms:
                print("DEBUG Row: ", row, " and Column: ", column, "have value: ", grid[row][column])
                if grid[row][column] == 1:
                    color = LIGHT_RED
                elif grid[row][column] == 2:
                    color = LIGHT_RED_2
                elif grid[row][column] == 3:
                    color = RED
                elif grid[row][column] == 4:
                    color = DARK_RED
                pygame.draw.rect(screen,
                                color,
                                [(MARGIN + WIDTH) * column + MARGIN,
                                (MARGIN + HEIGHT) * row + MARGIN,
                                WIDTH,
                                HEIGHT])

    # print("Just filled in the cells with red according to Opponent's data")
        
        # clock.tick(60)

    pygame.display.flip()


turn=0
while not done:

    

    event_sent = 0
    signal_move = 0
    data_for_move = ssl_sock.recv(1024)
    # print("DEBUG: size for data_for_move, " ,len(data_for_move))
    # print("DEBUG: value of data ", data_for_move)
    signal_move_prime = pickle.loads(data_for_move)
    # signal_move = signal_move_prime["signal"]
    print("Signal recieved from Server", signal_move_prime[0])


    clock.tick(60)

    screen.fill(LIGHT_GREEN_2)

    pygame.mouse.set_visible(True)

    

    otherPlayerAtoms = signal_move_prime[1]
    thisPlayerAtoms = signal_move_prime[3]
    grid = signal_move_prime[2]

    screenUpdate()

    c_turn = 0

    print("DEBUG: Player_win value is : ", signal_move_prime[4])



    

    # if signal_move_prime[0] == 0:
    #     screen.fill(RED)
    #     screenUpdate()
    #     pygame.display.flip()
    #     #When it's not the player's turn
    #     print("DEBUG: This is not my turn")
    #     another_flag_here = 0
    #     another_flag = ssl_sock.recv(1024)
    #     another_flag_here = pickle.loads(another_flag)
    #     print("DEBUG: Now i can play")
    #     if another_flag_here == 1:
    #         continue

    # print(type(signal_move_prime))

    print("DEBUG: This is before checking win condition, both the player should get this, win valus is: ", signal_move_prime[4])

    if(signal_move_prime[4] == 1):
        #player 1 won
        # Tk().wm_withdraw() #to hide the main window
        screen.fill(WHITE)
        pygame.display.flip()
        text = font.render('Player One Won', True, GREEN, WHITE) 
        textRect = text.get_rect()  
        textRect.center = (400 // 2, 400 // 2) 
        screen.blit(text, textRect)
        pygame.display.flip()
        screen.quit()

    if(signal_move_prime[4] == 2):
        #player 2 won
        # Tk().wm_withdraw() #to hide the main window
        screen.fill(WHITE)
        pygame.display.flip()
        text = font.render('Player Two Won', True, GREEN, WHITE) 
        textRect = text.get_rect()  
        textRect.center = (200 // 2, 200 // 2) 
        screen.blit(text, textRect)
        pygame.display.flip()
        screen.quit()




    while signal_move_prime[0] == 1:

        print("DEBUG: Got back in, since player clicked on the wrong cell")

        works = 0
        
        # print("DEBUG: This is where I am filling the screen green")
        screen.fill(GREEN)
        

        flag=0
        while flag!=1:
            for event in pygame.event.get():
            #Now we've got event of this client
                if event.type == pygame.QUIT:  # If user clicked close
                    event_sent = 1
                    done = True
                    flag = 1  # Flag that we are done so we exit this loop
                #Now we need to send a signal to server saying that this player has quit the game
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    event_sent = 2
                    pos = pygame.mouse.get_pos()
                    flag=1

        
       
               

        if event_sent == 1:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
            #Now we need to send a signal to server saying that this player has quit the game
        elif event_sent == 2:
            c_turn = c_turn+1
        # User clicks the mouse. Get the position
            # Change the x/y screen coordinates to grid coordinates
            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)

            if row >= 0 and row <=8 and column >=0 and column <= 8:

                print("DEBUG: Row and Column acquired : ", row, " ", column)

                if (row, column) in otherPlayerAtoms:
                    print("You can't click there, Click again")
                    works = 1
                else:
                    if (row, column) in thisPlayerAtoms:
                        print("It is already in the block")   
                        # Set that location to one
                        grid[row][column] = int(grid[row][column]) + 1
                        # print("DEBUG: only updated that particular cell, Value of row: ", row, " and column: ", column, " is: ", grid[row][column])
                        turn = turn + 1
                        checkForRowAndColumn(row, column, 1)
                        # print("Click ", pos, "Grid coordinates: ", row, column)
                        # print("thisPlayerAtoms are: ", thisPlayerAtoms)
                        # print("otherPlayerAtoms are: ", otherPlayerAtoms)
                    else:
                        # print("DEBUG: before updating the grid, the grid is: ", grid)
                        thisPlayerAtoms.append(tuple([row, column]))
                        # Set that location to one
                        grid[row][column] = int(grid[row][column]) + 1
                        # print(grid)
                        # print("DEBUG: only updated that particular cell, Value of row: ", row, " and column: ", column, " is: ", grid[row][column])
                        # print("DEBUG: the updated grid before the algorithm was executed is: ", grid)
                        # print("1234")
                        turn = turn + 1
                        checkForRowAndColumn(row, column, 1)
                        # print("DEBUG: The updated grid after the algorithm executed is, : ", grid)
                        # print("Click ", pos, "Grid coordinates: ", row, column)
                        # print("thisPlayerAtoms are: ", thisPlayerAtoms)
                        # print("otherPlayerAtoms are: ", otherPlayerAtoms)

            #This is where I have to send the data
            
            

            screenUpdate()
            print("DEBUG: Works is : ", works)

            if works == 0:
                print("DEBUG: User clicked on the right part")
                signal_move_prime[0] = 0
                sendDatatoServer(event_sent, thisPlayerAtoms, otherPlayerAtoms, grid, row, column)
                ret = ssl_sock.recv(1024)
                if pickle.loads(ret) == 0:
                    print("Error")
                
                #First getting the ok signal from the server
                another_flag = ssl_sock.recv(1024)
                another_flag_here = pickle.loads(another_flag)
                if(another_flag == -1):
                    messagebox.showinfo("You have tampered with the data, OK")
                break
            
            else:
                print("User didn't click on the right cell")


    print("DEBUG: Got out of that while loop now in the inner while loop")


    screen.fill(RED)

    c_turn=c_turn+1

    #Now Drawing it on the screen
    screenUpdate()

    
 
    # Limit to 60 frames per second
    clock.tick(60)
 
    pygame.mouse.set_visible(False)


    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # if signal_move_prime[0] == 0:
    #     screen.fill(RED)
    #     screenUpdate()
    #     pygame.display.flip()
    #     #When it's not the player's turn
    #     print("DEBUG: This is not my turn")
    #     another_flag_here = 0
    #     another_flag = ssl_sock.recv(1024)
    #     another_flag_here = pickle.loads(another_flag)
    #     print("DEBUG: Now i can play")
    #     if another_flag_here == 1:
    #         continue
        




ssl_sock.close()

