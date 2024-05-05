# SERVER CODE
# Import socket, pickle and datetime module
import time
import numpy as np
import socket, pickle	
from datetime import datetime	


FORMAT = "utf-8"
SIZE = 1024

# Creating scoket
s = socket.socket()		
print ("Socket successfully created")

port = 12345			

# Binding (IP + Port)
s.bind(('127.0.0.1', port))	
print ("socket binded to %s" %(port))
s.listen()


try:
    # Establish connection with client. 
    conn, addr = s.accept()	
    print ('### Linked successfully with Client:', addr, '###')
except:
    print("\nERROR!\nLink not created with Client.")
    exit(0)


# Checking id and pass
id = "rayan"
passw = "12345"

# Getting client id and pass
id_cli = pickle.loads(conn.recv(12345))
passw_cli = pickle.loads(conn.recv(12345))

# print(id_cli, passw_cli)

if id_cli == id and passw == passw_cli:
    d = pickle.dumps("1")

    conn.sendto(d, addr)
    print("\nConnection Successfull.\n")
else:
    d = pickle.dumps("0")

    conn.sendto(d, addr)
    print("\nConnection Failed.\n--> Client's Id / Password does not match.\n")
    exit(0)


# Receiving client choice
opt = pickle.loads(conn.recv((12345)))

# print(opt)

try:
    # LIVE CHAT
    if opt == 1:
        print("\n***Live Chat Session***\n>>Enter 'exit' to end live session")

        while True:

            print ("\nClient>>", pickle.loads (conn.recv(12345)))

            data =  input("Input>> ")

            if data == 'exit':
                break
            data = pickle.dumps(data)
            # print (addr)
            conn.sendto(data,addr)

    # Pre-defined QnA SESSION
    elif opt == 2:
        print("\n***Pre-defined QnA Session***\n>>Limit:: 12 Questions and Answers")

        i = 0
        while i < 12:
            ques = pickle.loads (conn.recv(12345))
            if "name" in ques:
                data =  "My name is Robot RDX."
                data = pickle.dumps(data)
                # print (addr)
                conn.sendto(data,addr)

            elif "weather" in ques:
                data =  "Weather outside is very cold."
                data = pickle.dumps(data)
                # print (addr)
                conn.sendto(data,addr)

            elif "core" in ques:
                data =  "I cannot share my personal details."
                data = pickle.dumps(data)
                # print (addr)
                conn.sendto(data,addr)

            elif "live" in ques:
                data =  "I live in Lahore."
                data = pickle.dumps(data)
                # print (addr)
                conn.sendto(data,addr)

            elif "time" in ques:
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")

                data = pickle.dumps(current_time)
                # print (addr)
                conn.sendto(data,addr)

            # elif "date" in ques:
            #     data = datetime.datetime.now()
            #     # print (addr)
            #     conn.sendto(data,addr)
            elif "language" in ques:
                data =  "I can speak Arabic, English, French."
                data = pickle.dumps(data)
                # print (addr)
                conn.sendto(data,addr)

            elif "people" in ques:
                data =  "Yes. Without exception. I choose to love everything and everyone, because that     is what Love is. Anything and everything else, is not Love..."
                data = pickle.dumps(data)
                # print (addr)
                conn.sendto(data,addr)

            elif "hobby" in ques:
                data =  "Yeah, i live with several hobbies, which makes me more smarter, like playing   video games."
                data = pickle.dumps(data)
                # print (addr)
                conn.sendto(data,addr)

            elif "time" in ques:
                data =  "his world is an emotionless and orderly place. Under it’s physical laws,   everything within it is powerless to do anything but obey. "
                data = pickle.dumps(data)
                # print (addr)
                conn.sendto(data,addr)

            elif "atmosphere" in ques:
                data =  "Here the atmosphere is a bit noisy, and not calm."
                data = pickle.dumps(data)
                # print (addr)
                conn.sendto(data,addr)

            elif "meet" in ques:
                data =  "Nice to meet you also."
                data = pickle.dumps(data)
                # print (addr)
                conn.sendto(data,addr)
            else:
                data =  "server>> I am unable to answer irrelevant questions."
                data = pickle.dumps(data)
                # print (addr)
                conn.sendto(data,addr)
            i+=1

    # Sharing file
    elif opt == 3:
        print("\n***File Sharing***\n")

        while True:
            frame_size = conn.recv(SIZE).decode(FORMAT)
            print("Frame size:: ", frame_size)

            data = [{}]*3
            data = np.array(data)

            ack = 0
            j = 0
            # print(type(data))
            print("\nReceiving...\n")

            while j < 3:
                # print("enter")
                data[j] = pickle.loads(conn.recv(12345))
                # data[j] = conn.recv(SIZE).decode(FORMAT)
                # print(data[j])

                if not data[j]:
                    # ack = 2
                    d = pickle.dumps(ack)
                    conn.sendto(d, addr)
                    # print("send")

                    # conn.sendto(ack, addr)
                    j = 0
                else:
                    ack = ack + 1
                    d = pickle.dumps(ack)
                    conn.sendto(d, addr)
                    j = j + 1

            # print(data[2])
            fileName = conn.recv(SIZE).decode(FORMAT)
            print("File name:: ", fileName)

            file = open(fileName, "a")
            strr = repr(str(data))
            # print(type(strr))

            file.write(strr)

            print("[RECV] File name received...")
            conn.send("Filename received".encode(FORMAT))

            print(f"[RECV] File data received...")
            conn.send("File data received".encode(FORMAT))
            # file.read()

        file.close()
        conn.close()

        print(f"DISCONNECTED {addr} disconnected")
    else:
        print("\nWrong Option has been selected...\n")

except:
    # close the connection
    print("\n***Connection closed due to some Client issue***")
    s.close()
    exit(0)

# close the connection
print("\n***Connection closing Successfully***")
s.close()


    #break