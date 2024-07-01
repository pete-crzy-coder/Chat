import socket
import threading

# Server configuration
HOST = '0.0.0.0'
PORT = 5001

class chat_client:
    def __init__(self, name, address, socket):
        self.name = name
        self.address = address
        self.socket = socket

# List to store client sockets
client_details = {}
name_to_address = {}
addcli = []

client_counter = 1

def broadcast(message, exclude_names = []):
    for client in client_details.values():
        if (client.name not in exclude_names):
            client.socket.send(message.encode("utf-8"))

def set_name_action(client_address, name):
    name = name.replace(" ", "")
    client = client_details[client_address]

    if name not in name_to_address and name_to_address[client.name] == client_address:
        del name_to_address[client.name]
        client.name = name
        name_to_address[name] = client_address
    else:
        client.socket.send(f"Cannot set_name to {name}. It is used by another client.")

def secret_message_action(client_address, receiver_name, message):
    sender = client_details[client_address]
    receiver = client_details[name_to_address[receiver_name]]
    if receiver:
        receiver.socket.send(f"{sender.name} says: {message}")


def process_message(client_address, message):
    if message.startswith("/"):
        # client send a command
        arguments = message.split()
        match arguments[0]:
            case '/set_name':
                return set_name_action(client_address, arguments[1])
            case '/secret':
                return secret_message_action(client_address, arguments[1], arguments[2])

        return

    client = client_details[client_address]
    broadcast(f"{client.name} says: {message}", [client.name])

# Function to handle client connections
def handle_client(client_socket, client_address):
    global client_counter
    print(f"[*] {client_address} connected.")

    # Add client socket to the list
    auto_client_name = f"Unnamed_{client_counter}"
    client = chat_client(auto_client_name, client_address, client_socket)
    client_details[client_address] = client
    name_to_address[auto_client_name] = client_address

    client_counter += 1

    broadcast(f"Welcome user {auto_client_name}.")

    # Receive and broadcast messages
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break

            print(f"[{client_address}] {message}")

            process_message(client_address, message)

        except:
            # Remove the client from the list if there's an error or client disconnects
            print(f"[*] {client_address} disconnected.")
            client_details.remove(client_address)
            client_socket.close()
            broadcast(f"{client.name} disconnected.")
            break

# Function to start the server
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"[*] Server listening on {HOST}:{PORT}")

    while True:
        client_socket, client_address = server.accept()
        addcli.append(client_address)
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

if __name__ == "__main__":
    start_server()