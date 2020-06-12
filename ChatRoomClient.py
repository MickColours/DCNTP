'''
The client should both receive and send data in multiple threads:

1 for receiving:
    -constantly (while True) checks to see if a message has been received by the server(the server
    is actually sending the message it just received back out) and displays the messgae
    along with who sent the message
        -the fact that the sender's ID is received with every message means that it is
        likely that every message sent from a client also contains the information
        about the client's ID

1 for sending:
    -Constantly (while True) awaiting input from the user to be sent to the server to
    be redistributed back to every *OTHER* client - messages sent from the client should
    not be sent back to itself

Other requirements:

    -Client automatically joins when program is run - and then possibly immediately prompted
    for information to ID the current client as (Username)

    -User can "leave" the chatroom at any time by inputting a certain phrase (!Quit) - likely
    just a sys.exit() if the message *CONTENT*(without header) read is equivalent to
    the phrase

Written by David McCullers
'''

import sys
import socket
import threading



serverName = "127.0.0.1"
serverPort = 5678


client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setblocking(False)
#client_socket.connect(serverName, serverPort)

HEAD_LEN = 5
USR_LEN = 2

username = bytes(input("Username: "), "utf-8")

class recvThread (threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID


    def run(self):
        print("Receiving messages:")
        try:
            recv_message()
            print("can't do the recv")
        except:
            pass


class sendThread (threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID

    def run(self):
        print ("Starting " + self.name)
        while True:
            messageToSend = bytes(input("> "), "utf-8")
            if "!join" not in messageToSend.decode("utf-8"):
                if "!terminate" not in messageToSend.decode("utf-8"):
                    if "!quit" in messageToSend.decode("utf-8"):
                        send_message(messageToSend)
                        sys.exit()
                    else:
                        send_message(messageToSend)



def send_message(message):
    message = username + bytes(" ", "utf-8") + message
    msg_header = f"{len(message) : {HEAD_LEN}}".encode("utf-8")
    usr_header = f"{len(username): {USR_LEN}}".encode("utf-8")
    message = msg_header + usr_header + message


    client_socket.sendto(message, (serverName, serverPort))

def recv_message():
    try:
        message, clientAddress = client_socket.recvfrom(2048)
        username_len = int(message[HEAD_LEN:(HEAD_LEN + USR_LEN)].decode("utf-8").strip())
        sender_username = message[(HEAD_LEN + USR_LEN): HEAD_LEN + USR_LEN + username_len].decode("utf-8")
        message = message[(HEAD_LEN + USR_LEN + username_len):].decode("utf-8")

        if "!terminate" in message:
           sys.exit()
        else:
            print("\n" + sender_username + ">" + message)
    except:
        try:
            print(message.decode("utf-8"))
        except:
            pass
    threading.Timer(1.0, recv_message).start()


send_thread = sendThread(1)

recv_thread = recvThread(2)

send_message(bytes("!join", "utf-8"))
send_message(bytes("!users", "utf-8"))
recv_thread.start()
send_thread.start()

