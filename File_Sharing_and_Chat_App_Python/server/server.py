from socket import *
from threading import *
import pickle

clients = set()

def clientThread(clientSocket, clientAddress):
    while True:
        message = clientSocket.recv(1024).decode("utf-8")
        print(clientAddress[0] + ":" + str(clientAddress[1]) +" says: "+ message)
        for client in clients:
            clientMessage = str(input("data> "))
            clientSocket.send(clientMessage.encode("utf-8"))

        if not message:
            clients.remove(clientSocket)
            print(clientAddress[0] + ":" + str(clientAddress[1]) +" disconnected")
            break

    clientSocket.close()

hostSocket = socket(AF_INET, SOCK_STREAM)
hostSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR,1)

hostIp = "127.0.0.1"
portNumber = 7500
hostSocket.bind((hostIp, portNumber))
hostSocket.listen()
print ("Waiting for connection...")


while True:
    try:
        # Establish connection with client. 
        clientSocket, clientAddress = hostSocket.accept()
        print ('### Linked successfully with Client:',clientAddress, '###')
        clients.add(clientSocket)
    except:
        print("\nERROR!\nLink not created with Client.")
        exit(0)
        
    # Checking id and pass
    # id = "rayan"
    # passw = "12345"

    # # Getting client id and pass
    # id_cli = pickle.loads(clientSocket.recv(7500))
    # passw_cli = pickle.loads(clientSocket.recv(7500))

    # # print(id_cli, passw_cli)

    # if id_cli == id and passw == passw_cli:
    #     d = pickle.dumps("1")

    #     clientSocket.sendto(d, clientAddress)
    #     print("\nConnection Successfull.\n")
    # else:
    #     d = pickle.dumps("0")

    #     clientSocket.sendto(d, clientAddress)
    #     print("\nConnection Failed.\n--> Client's Id / Password does not match.\n")
    #     exit(0)

    print ("Connection established with: ", clientAddress[0] + ":" + str(clientAddress[1]))
    thread = Thread(target=clientThread, args=(clientSocket, clientAddress, ))
    thread.start()