import pickle
import re
from socket import *
import sys
import ssl
import pprint
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


#Use these functions to send or recieve data
#send
# data = pickle.dumps(data_to_be_sent_in_whatever_format)
# ssl_sock.send(data)
#receive
# data_from_server = ssl_sock.recv(1024)
# data = pickle.loads (data_from_server)


ssl_sock.close()


    #name=gethostbyname(gethostname())
    #print(name)
    #print(gethostname())
#except :
#	print("Connection error")
	