# CLIENT CODE
# My ID : rayan
# My Password : 12345

# Import socket and pickle module
import time
import socket
import pickle

global ray
ray = 0
# define the countdown func.
def countdown(t):
    print("\nSending ...")
    print("\n***CountDown***")
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1

    print("\n***TimeOut***")
    ack = pickle.loads(s.recv(11122))
    print(ack)

    if str(ack) == "1":
        return 1
    else:
        return 0


FORMAT = "utf-8"
SIZE = 1024

# Create a socket object
s = socket.socket()
# Binding (IP + Port)  --> Optional
clientAdress = ('127.0.0.1', 11122)
s.bind(clientAdress)

# 192.168.48.50

# Define the port on which you want to connect
ip = '127.0.0.1'
port = 12345

addr = (ip, port)


# connect to the server on local computer

try:
    # Establish connection with server.
    s.connect(addr)
    print('### Linked successfully with Server ###')
except:
    print("\nERROR!\nLink not created with Server.")
    exit(0)


# Checking id and pass
print("\n~~~LOGIN~~~")
id = input("\nEnter your id: ")
passw = input("Enter your pass: ")

s.sendto(pickle.dumps(id), addr)
s.sendto(pickle.dumps(passw), addr)

d = pickle.loads(s.recv(11122))

if d == "1":
    print("\n\nConnection Successfull.\n")
elif d == "0":
    print("Connection failed!\n--> Id / Password does not match with server.\n")
    exit(0)


# Client choice
print("1. Do you want to do Live chat?\n2. Do you want to do predefined QnA session?\n3. Do you want to share file?")
opt = int(input("Select Option (1 or 2 or 3):: "))

# Sending choice
s.sendto(pickle.dumps(opt), addr)

try:
    # LIVE CHAT
    if opt == 1:
        print("\n***Live Chat Session***\n>>Enter 'exit' to end live session")

        while True:

            ques = input("\nInput>> ")

            if ques == 'exit':
                break

            data = pickle.dumps(ques)
            s.sendto(data, addr)
            print("Server>> ", pickle.loads(s.recv(11122)))

    # Pre-defined QnA SESSION
    elif opt == 2:
        print("\n***Pre-defined QnA Session***\n>>Limit:: 12 Questions and Answers")

        i = 0
        while i < 12:
            print("\n")
            print("Question No.::", str((i+1)))
            ques = input("Enter your question: ")
            data = pickle.dumps(ques)
            s.sendto(data, addr)
            print(pickle.loads(s.recv(11122)))
            i += 1

    # Sharing file
    elif opt == 3:
        print("\n***File Sharing***\n")
        ack = 1
        count = 0

        while ack == 1:
            ret = 0
            rand_num = input("Input a Random number for simulate statistically(0 - 99): ")
            print()
            name = input("Enter File name you want to share: ")

            count = count + 1

            if name == 'exit':
                break

            try:
                file = open("data/"+name, "r")
            except:
                print("\nNOT FOUND.\nFile name you entered not exists...\n")
                exit(0)

            data = file.read()

            s.send(name.encode(FORMAT))
            s.send(data.encode(FORMAT))
            s.send(rand_num.encode(FORMAT))

            bol = True
            while bol == True:
                ack1 = countdown(int(5))
                print(ack1)
            
                if ack1 == 1:
                    msg = s.recv(SIZE).decode(FORMAT)
                    print(f"[SERVER]: {msg}")

                    msg = s.recv(SIZE).decode(FORMAT)
                    print(f"[SERVER]: {msg}")

                    print("File Transfered Successfully...\n")
                    bol = False

                    d = pickle.loads(s.recv(11122))
                    print("No. of files send succesfully: ", d)
                    print()
                else:
                    ret = ret + 1
                    print("\nReTransmitting...")
                    s.send(name.encode(FORMAT))
                    s.send(data.encode(FORMAT))
                    if ret >= 2:
                        print("File Transmission unsuccessful")
                        exit(0)


        print("Total No. of files send succesfully: ", d)
        print("Total No. of files lost: ", (count-d))
        file.close()

    else:
        print("\nSORRY! Wrong Option selected...\n")


except:
    # close the connection
    print("\n***Connection closed due to some Server issue***")
    s.close()
    exit(0)

# close the connection
print("\n***Connection closed Successfully***")
s.close()
