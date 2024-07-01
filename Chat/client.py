# Import socket module
import socket
from threading import Thread

# In this Line we define our local host
# address with port number
SERVER = "127.0.0.1"
PORT = 5001
# Making a socket instance
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connect to the server
s.connect((SERVER, PORT))
clientMessage = None

print('Write "_exit" to terminate.')

def sender():
    while True:
        Me = input()
        if Me == '_exit':
            s.close()
            break
        s.sendall(Me.encode("utf-8"))


def receiver():
    global clientMessage
    while True:
        if clientMessage != '_exit':
            message = s.recv(1024).decode('utf-8')
            print(message)
        else:
            break

if __name__ == '__main__':
    e = Thread(target = sender).start()
    r = Thread(target = receiver).start()

