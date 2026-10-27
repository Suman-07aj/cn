import socket

# --- Original Orthogonal Codes ---
c1 = [1, 1, 1, 1]
c2 = [1, -1, 1, -1]

HOST = '127.0.0.1'
PORT = 65432

# Set up server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(2)

print("Server (Channel/Receiver) is running... Waiting for Client 1 & Client 2...")

# Accept Client 1
conn1, addr1 = server_socket.accept()
print("Client 1 connected from:", addr1)
d1 = int(conn1.recv(1024).decode())

# Accept Client 2
conn2, addr2 = server_socket.accept()
print("Client 2 connected from:", addr2)
d2 = int(conn2.recv(1024).decode())

# --- Modulation ---
c1_m = [1, 1, 1, 1]
c2_m = [1, -1, 1, -1]

if d1 == 0:
    c1_m = [-(x) for x in c1]
if d2 == 0:
    c2_m = [-(x) for x in c2]

print("\nModulated codes:", c1_m, c2_m)

# --- Channel Summation ---
sum1 = []
for x1, x2 in zip(c1_m, c2_m):
    sum1.append(x1 + x2)

print("Combined Channel Signal (sum1):", sum1)

# --- Receiver Decoding ---
t1 = 0
t2 = 0
for x1, x2 in zip(sum1, c1):
    t1 += (x1 * x2)    
for x1, x2 in zip(sum1, c2):
    t2 += (x1 * x2)

print("t1:", t1)
print("t2:", t2)

if t1 >= 0:
    print("data bit is 1 in client 1")
elif t1 < 0:
    print("data bit is 0 in client 1")

if t2 >= 0:
    print("data bit is 1 in client 2")
else:
    print("data bit is 0 in client 2")

conn1.close()
conn2.close()
server_socket.close()