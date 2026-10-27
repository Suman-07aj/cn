import socket

HOST = '127.0.0.1'
PORT = 65432

data_bit = input("Enter data bit (0 or 1): ")

# Connect to Server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Send the data bit to the server
client_socket.sendall(data_bit.encode())
print("Data bit sent successfully!")

client_socket.close()