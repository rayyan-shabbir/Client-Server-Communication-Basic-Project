from tkinter import *
from socket import *
from tkinter import filedialog
from tkinter import messagebox
import os
import pickle
from threading import *


root = Tk()
root.title("FirReM-RDX-M02")
root.geometry("950x600+700+200")
root.configure(bg="black")
root.resizable(False, False)

def login(clientSocket, hostIp, portNumber):
    addr = (hostIp, portNumber)
    # Checking id and pass
    window = Tk()
    window.geometry('350x460+400+200')
    window.title("~~~LOGIN~~~")

    def check():
        ID = id.get()
        Passwd = passwd.get()
        clientSocket.sendto(pickle.dumps(ID), (addr))
        clientSocket.sendto(pickle.dumps(Passwd), (addr))

        # print("\n~~~LOGIN~~~")
        # id = input("\nEnter your id: ")
        # passw = input("Enter your pass: ")

        d = pickle.loads(clientSocket.recv(11122))

        if d == "1":
            print("\n\nConnection Successfull.\n")
            return True
        elif d == "0":
            print("Connection failed!\n--> Id / Password does not match with server.\n")
            exit(0)

    # Hbackground = PhotoImage(file='Images/receiver.png')
    # Label(window, image=Hbackground).place(x=-2, y=0)

    Label(window, text="Enter your ID", font=('arial', 10, 'bold'), bg="#f4fdfe").place(x=30, y=240)

    id = Entry(window, width=25, fg="black", border=2, bg="white", font=('arial', 15))
    id.place(x=20, y=270)
    id.focus()

    Label(window, text="Enter your password ", font=('arial', 10, 'bold'), bg="#f4fdfe").place(x=30, y=300)

    passwd = Entry(window, width=25, fg="black", border=2, bg="white", font=('arial', 15))
    passwd.place(x=20, y=330)

    btnSendMessage = Button(window, text="Send", width=20, command=check)
    btnSendMessage.grid(row=2,column=0, padx=10, pady=10)



    # window.mainloop()

def Chat():
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    hostIp = "127.0.0.1"
    portNumber = 7500

    window = Tk()

    try:
        clientSocket.connect((hostIp, portNumber))
        window.title("Connected To: "+ hostIp+ ":"+str(portNumber))
    except:
        window.title("\nERROR!\nLink not created with Server.")
        exit(0)
        

    # START
    # login(clientSocket, hostIp, portNumber)
    # Checking id and pass
    # print("\n~~~LOGIN~~~")
    # id = input("\nEnter your id: ")
    # passw = input("Enter your pass: ")

    # clientSocket.sendto(pickle.dumps(id), (hostIp, portNumber))
    # clientSocket.sendto(pickle.dumps(passw), (hostIp, portNumber))

    # d = pickle.loads(s.recv(11122))

    # if d == "1":
    #     print("\n\nConnection Successfull.\n")
    # elif d == "0":
    #     print("Connection failed!\n--> Id / Password does not match with server.\n")
    #     exit(0)
    
    # FINISH


    txtMessages = Text(window, width=50, bg="#202A44")
    txtMessages.grid(row=0, column=0, padx=10, pady=10)

    txtYourMessage = Entry(window, width=50)
    txtYourMessage.insert(0,"Type message")
    txtYourMessage.grid(row=1, column=0, padx=10, pady=10)

    def sendMessage():
        clientMessage = txtYourMessage.get()
        txtMessages.insert(END, "\n" + "You: "+ clientMessage)
        clientSocket.send(clientMessage.encode("utf-8"))

    btnSendMessage = Button(window, text="Send", width=20, command=sendMessage, bg="green", fg="white")
    btnSendMessage.grid(row=2, column=0, padx=10, pady=10)

    def recvMessage():
        while True:
            serverMessage = clientSocket.recv(1024).decode("utf-8")
            print(serverMessage)
            txtMessages.insert(END, "\n"+serverMessage)

    recvThread = Thread(target=recvMessage)
    recvThread.daemon = True
    recvThread.start()

    window.mainloop()

    


# Creating function for Sending
def Send():
    window = Toplevel(root)
    window.title("Send")
    window.geometry("950x600+700+200")
    window.configure(bg="black")
    window.resizable(False, False)

    # Creating function for selecting file
    def select_file():
        global filename
        filename = filedialog.askopenfile(initialdir = os.getcwd, title = "Select Image File", filetype =(('file_type', '*.txt'), ('all files', '*.*')))

    # Creating function for sending file
    def sender():
        s = socket.socket()
        host = gethostname()
        # host = socket.gethostname()

        port = 8080
        s.bind((host, port))

        s.listen(1)
        print(host)
        print('Waiting for any incoming connection...')
        conn, addr = s.accept()

        file = open(filename, 'rb')
        file_data = file.read(1024)

        conn.send(file_data)

        print("Data has been sent successfully...")

    # Icon
    image_icon1 = PhotoImage(file='Images/send3.png')
    window.iconphoto(False, image_icon1)

    Label(window, text="Send File", font=('Acumin Variable Concept', 30, 'bold'),fg="white").place(x=50, y=40)

    Sbackground = PhotoImage(file='Images/sender1.png')
    Label(window, image=Sbackground).place(x=-2, y=0)

    Mbackground = PhotoImage(file='Images/id11.png')
    Label(window, image=Mbackground, bg='#f4fdfe').place(x=170, y=90)

    host = gethostname()
    # host = socket.gethostname()

    Label(window, text=f'ID: {host}', bg='black', height=1, font='arial 14 bold', fg='white').place(x=360, y=140)

    Button(window, text="+ attach file", width=10, height=1, font='arial 14 bold', bg='white', fg='black', command=select_file).place(x=310, y=470)
    Button(window, text="SEND", width=8, height=1, font='arial 14 bold', bg='red', fg='#fff', command=sender).place(x=480, y=470)

    window.mainloop()


# Creating function for Receiving
def Receive():
    main = Toplevel(root)
    main.title("Receive")
    main.geometry("950x600+700+200")
    main.configure(bg='#f4fdfe')
    main.resizable(False, False)

    def receiver():
        ID = SenderID.get()
        filename1 = incoming_file.get()

        s = socket.socket()
        port = 8080
        s.connect((ID, port))

        file = open(filename1, 'wb')

        file_data=s.recv(1024)
        file.write(file_data)

        file.close()
        print("File has been received successfully")

    # Icon
    image_icon1 = PhotoImage(file='Images/receive.png')
    main.iconphoto(False, image_icon1)

    Hbackground = PhotoImage(file='Images/receiver1.png')
    Label(main, image=Hbackground).place(x=-2, y=0)

    logo = PhotoImage(file='Images/profile1.png')
    Label(main, image=logo, bg="#f4fdfe").place(x=20, y=260)    

    Label(main, text="Receive", font=('arial', 20), bg="#f4fdfe").place(x=130, y=300)

    Label(main, text="Input sender id", font=('arial', 10, 'bold'), bg="#f4fdfe").place(x=20, y=370)
    SenderID = Entry(main, width=25, fg="black", border=2, bg="white", font=('arial', 15))
    SenderID.place(x=20, y=400)
    SenderID.focus()

    Label(main, text="filename for the incoming file: ", font=('arial', 10, 'bold'), bg="#f4fdfe").place(x=20, y=450)
    incoming_file = Entry(main, width=25, fg="black", border=2, bg="white", font=('arial', 15))
    incoming_file.place(x=20, y=480)

    imageicon = PhotoImage(file="Images/arrow.png")
    rr = Button(main, text = "Receive", compound=LEFT, image=imageicon, width=130, bg="green", font=('arial', 14, 'bold'), command=receiver)

    rr.place(x=20, y=530)

    main.mainloop()

# Icon
image_icon = PhotoImage(file="Images/icon1.png")
root.iconphoto(False, image_icon)


Label(root, text="File Transfer & Chat Application", font=('Acumin Variable Concept', 30, 'bold'),fg="white", bg="black").place(x=20, y=30)

Frame(root, width=400, height=2, bg="#f3f5f6").place(x=25, y=80)

send_image = PhotoImage(file="Images/send01.png")
send = Button(root, image=send_image, bg="black", bd=0, command=Send)
send.place(x=110, y=110)


receive_image = PhotoImage(file="Images/receive3.png")
receive = Button(root, image=receive_image, bg="black", bd=0, command=Receive)
receive.place(x=400, y=100)

chat_image = PhotoImage(file="Images/chat2.png")
chat = Button(root, image=chat_image, bg="black", bd=0, command=Chat)
chat.place(x=695, y=110)


# Label
Label(root, text="Send", font=('Helvetica', 20, 'bold'), fg="white", bg="black").place(x=125, y=225)
Label(root, text="Receive", font=('Helvetica', 20, 'bold'), fg="white", bg="black").place(x=407, y=230)
Label(root, text="Chat", font=('Helvetica', 20, 'bold'), fg="white", bg="black").place(x=733, y=230)

background = PhotoImage(file="Images/bg2.png")
Label(root, image=background).place(x=-2, y=295)

root.mainloop()