import pickle, re
import sys
import ssl
from socket import *
import threading
from threading import Thread

ports=60000
namereg=re.compile("^[a-zA-Z0-9]{0,20}$")
LOCALHOST="127.0.0.1"
server_port= 49999
buffer=[]
userlist={}
occupied_ports=[]
threads=[]

def client_port(portn, clientname):
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

    sentence=pickle.dumps("Your are added in Buffer")
    connssl.send(sentence)
    #break
    buffer.append(clientname)
    connssl.shutdown(SHUT_RDWR)
    connssl.close()




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
            t=Thread(target=client_port, args=(currport,currname,))
            t.start()
    except:
        print("Error")
        sys.exit(0)
        