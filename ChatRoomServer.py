'''
    -Server greets new user
    -Server tells all other clients currently connected that a new user has connected

    -Server tells all other clients when a currently connected client disconnects

    -Whenever a message is received by the server - it is sent to all users except the sender
        -Unique ID identified by client should be carried and broadcasted to other users
        with the message

Written by David McCullers
'''

import socket
serverPort = 5678

HEAD_LEN = 5
USR_LEN = 2

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(("127.0.0.1", serverPort))

print ("Server is running...")

client_list = {}


def recv_msg():
    try:
        msg, clientAddress = server_socket.recvfrom(2048)


        if msg:

            msg_length = int(msg[:HEAD_LEN].decode("utf-8").strip())
            usr_length = int(msg[HEAD_LEN:(HEAD_LEN + USR_LEN)].decode("utf-8").strip())

            client_username = msg[(HEAD_LEN + USR_LEN):]
            client_username = client_username[:usr_length].decode("utf-8")

            if len(msg[USR_LEN + HEAD_LEN:].decode("utf-8")) != msg_length:
                print("error here")
                return False

            if clientAddress not in client_list:
                client_list[clientAddress] = client_username
                print(client_list)
            return msg, clientAddress
        else:
            return False

    except:
        return False


while True:

    try:
        message, address = recv_msg()

        print(message)

        if message:
            if "!join" in message.decode("utf-8"):
                print("there's a !join")
                newJoinedUser = (client_list[address] + " has joined the server").encode("utf-8")
                welcomeUser = ("Welcome to the server " + client_list[address] + "!").encode("utf-8")

                for client in client_list:

                    if(client == address):
                        server_socket.sendto(welcomeUser, client)
                    else:
                        server_socket.sendto(newJoinedUser, client)

            elif "!quit" in message.decode("utf-8"):
                print("there's a !quit")
                userDC = (client_list[address] + " has disconnected from the server").encode("utf-8")
                for client in client_list:

                    if(client == address):
                        print("Removing " + str(client) + " from client list")
                        server_socket.sendto(bytes("!terminate", "utf-8"), client)
                        print("!terminate sent")
                        del client_list[client]
                        print("Client successfully removed")
                    else:
                        print("Notifying client...")
                        server_socket.sendto(userDC, client)

            elif "!users" in message.decode("utf-8"):
                stringUsrList = (str(list(client_list.values())))
                userList = ("Connected Users: " + stringUsrList).encode("utf-8")
                server_socket.sendto(userList, address)
            else:
                for client in client_list:
                    if(client == address):
                        continue
                    else:
                        server_socket.sendto(message, client)
        else:
            pass
    except:
        pass