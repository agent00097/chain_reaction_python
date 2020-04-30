import pickle
import re
from socket import *
import sys
import ssl
import pprint
a=[[0]*6 for i in range(11)]
b=[]
regex=re.compile("^[a-zA-Z0-9]{0,20}$")

username=input("Give username : ")
while regex.match(username) is None:
    username=input("Invalid input, please Re-Enter username : ")


b.append(username)
b.append(gethostbyname(gethostname()))
b.append(gethostname())

data=pickle.dumps(b)
serverName = '127.0.0.1'
serverPort = 49999
clientSocket = socket(AF_INET, SOCK_STREAM)
#clientSocket.bind(("127.0.0.1", 40000))
clientSocket.settimeout(10)
try:
    ssl_sock = ssl.wrap_socket(clientSocket,ca_certs="server.crt",cert_reqs=ssl.CERT_REQUIRED)
except:
    print("SSL error in wrap sockets")
    sys.exit(0)
try:
    ssl_sock.connect((serverName,serverPort))
except:
    print("Connection Error")
    sys.exit(0)

######Printing SSL
print (repr(ssl_sock.getpeername()))
print (ssl_sock.cipher())
print (pprint.pformat(ssl_sock.getpeercert()))
######Printing SSL


try:
    ssl_sock.send(data)
    modifieddata = ssl_sock.recv(1024)
    data=pickle.loads(modifieddata) 
    print(data)
    ssl_sock.close()
except:
    print("Error in sending or receiving data")
    sys.exit(0)


if data == -1:
    print("Name is already there in buffer")
    sys.exit(0)

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

data=pickle.dumps(1)
ssl_sock.send(data)
modifieddata = ssl_sock.recv(1024)
data=pickle.loads(modifieddata) 
print(data)

while data != "Ready":
    modifieddata = ssl_sock.recv(1024)
    data=pickle.loads(modifieddata)
    print(data) 

modifieddata = ssl_sock.recv(1024)
data=pickle.loads(modifieddata)
print(data) 

ssl_sock.close()


    #name=gethostbyname(gethostname())
    #print(name)
    #print(gethostname())
#except :
#	print("Connection error")
	