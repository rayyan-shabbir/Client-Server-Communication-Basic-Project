# SERVER CODE
# Import socket, pickle and datetime module
import time
import socket, pickle	
from datetime import datetime	
import random


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
                data =  "server>> My name is Robot RDX."
                data = pickle.dumps(data)
                # print (addr)
                conn.sendto(data,addr)

            elif "weather" in ques:
                data =  "server>> Weather outside is very cold."
                data = pickle.dumps(data)
                # print (addr)
                conn.sendto(data,addr)

            elif "core" in ques:
                data =  "server>> I cannot share my personal details."
                data = pickle.dumps(data)
                # print (addr)
                conn.sendto(data,addr)

            elif "live" in ques:
                data =  "server>> I live in Lahore."
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
                data =  "server>> I can speak Arabic, English, French."
                data = pickle.dumps(data)
                # print (addr)
                conn.sendto(data,addr)

            elif "people" in ques:
                data =  "server>> Yes. Without exception. I choose to love everything and everyone, because that     is what Love is. Anything and everything else, is not Love..."
                data = pickle.dumps(data)
                # print (addr)
                conn.sendto(data,addr)

            elif "hobby" in ques:
                data =  "server>> Yeah, i live with several hobbies, which makes me more smarter, like playing   video games."
                data = pickle.dumps(data)
                # print (addr)
                conn.sendto(data,addr)

            elif "time" in ques:
                data =  "server>> This world is an emotionless and orderly place. Under it’s physical laws,   everything within it is powerless to do anything but obey. "
                data = pickle.dumps(data)
                # print (addr)
                conn.sendto(data,addr)

            elif "atmosphere" in ques:
                data =  "server>> Here the atmosphere is a bit noisy, and not calm."
                data = pickle.dumps(data)
                # print (addr)
                conn.sendto(data,addr)

            elif "meet" in ques:
                data =  "server>> Nice to meet you also."
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

        count_rec = 0
        count_lost = 0
        rand_gen = random.randint(0, 99)
        while True:

            if count_lost > 0:
                ack1 = pickle.dumps(ack)
                conn.sendto(ack1, addr)
                time.sleep(1)
            

            filename = data = ""
            
            print("Threshhold:: ", rand_gen)
            filename = conn.recv(SIZE).decode(FORMAT)
            data = conn.recv(SIZE).decode(FORMAT)
            rand_num = conn.recv(SIZE).decode(FORMAT)
            # print(filename)

            if (rand_gen >= int(rand_num)) and filename != "" and data != "":
                    ack = pickle.dumps("1")
                    print("Receiving...")
                    time.sleep(6)
                    conn.sendto(ack, addr)

                    print("File name:: ", filename)
                    print("[RECV] File name received...")
                    file = open("server_data/"+filename, "w")
                    conn.send("Filename received".encode(FORMAT))

                    print(f"[RECV] File data received...")
                    file.write(data)
                    conn.send("File data received".encode(FORMAT))

                    print()
                    count_rec = count_rec + 1
                    print("No. of files received:: ", count_rec)
                    cr = pickle.dumps(count_rec)
                    conn.sendto(cr,addr)
            else:
                print("Packet is lost and its probability is: ", float(rand_gen), "%")
                count_lost = count_lost + 1
                ack = "0"
                print(ack)
                ack1 = pickle.dumps(ack)
                conn.sendto(ack1, addr)
                print("No. of files lost:: ", count_lost)

                time.sleep(10)
                
                print()
                if filename=='exit' or count_lost > 3:
                    print("Max files are lost :: ", count_lost)
                    conn.close()


        file.close()

        print("Total No. of files received:: ", count_rec)
        print("Total No. of files lost:: ", count_rec)
        conn.close()

        print(f"DISCONNECTED {addr} disconnected")
    else:
        print("\nWrong Option has been selected...\n")

except:
    # close the connection
    print("File does not received")
    print("\n***Connection closed due to some Client issue***")
    s.close()
    exit(0)

# close the connection
print("\n***Connection closing Successfully***")
s.close()


    #break