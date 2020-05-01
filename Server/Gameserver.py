import pickle, re, time
import sys
import ssl
from socket import *
import threading
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

    def run(self):
        player1=connbuffer[self.play1]
        player2=connbuffer[self.play2]
        data=pickle.dumps("Ready")
        player1.send(data)
        player2.send(data)
        data=pickle.dumps(self.play1)
        player2.send(data)
        data=pickle.dumps(self.play2)
        player1.send(data)
    
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
        