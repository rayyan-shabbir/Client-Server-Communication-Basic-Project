import time

# define the countdown func.
def countdown(t):
    
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1
      
    print('Fire in the hole!!')
  
  
# input time in seconds
t = input("Enter the time in seconds: ")
  
# function call
countdown(int(t))


# def Chat():
#     # CLIENT CODE

#     FORMAT = "utf-8"
#     SIZE = 1024

#     # Create a socket object
#     s = socket.socket()

#     # Binding (IP + Port)  --> Optional
#     clientAdress = ('127.0.0.1', 11122)
#     s.bind(clientAdress)

#     # 192.168.48.50

#     # Define the port on which you want to connect
#     ip = '127.0.0.1'
#     port = 12345

#     addr = (ip, port)


#     # connect to the server on local computer

#     try:
#         # Establish connection with server.
#         s.connect(addr)
#         print('### Linked successfully with Server ###')
#     except:
#         print("\nERROR!\nLink not created with Server.")
#         exit(0)


#     # Checking id and pass
#     print("\n~~~LOGIN~~~")
#     id = input("\nEnter your id: ")
#     passw = input("Enter your pass: ")

#     s.sendto(pickle.dumps(id), addr)
#     s.sendto(pickle.dumps(passw), addr)

#     d = pickle.loads(s.recv(11122))

#     if d == "1":
#         print("\n\nConnection Successfull.\n")
#     elif d == "0":
#         print("Connection failed!\n--> Id / Password does not match with server.\n")
#         exit(0)


#     try:
#         # LIVE CHAT
#         print("\n***Live Chat Session***\n>>Enter 'exit' to end live session")

#         while True:

#             ques = input("\nInput>> ")

#             if ques == 'exit':
#                 break

#             data = pickle.dumps(ques)
#             s.sendto(data, addr)
#             print("Server>> ", pickle.loads(s.recv(11122)))

    
#     except:
#         # close the connection
#         print("\n***Connection closed due to some Server issue***")
#         s.close()
#         exit(0)

#     # close the connection
#     print("\n***Connection closed Successfully***")
#     s.close()
