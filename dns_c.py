import socket

s = socket.socket()
s.connect(("127.0.0.1", 5000))

domain = input("Enter domain: ")
s.send(domain.encode())

print("IP Address:", s.recv(1024).decode())
s.close()