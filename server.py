
import socket
import threading
import json
from crc import verify

HOST = "127.0.0.1"
PORT = 5001


def handle_client(conn, addr):
    print("\nConnected:", addr)

    try:
        data = conn.recv(4096).decode()
        packet = json.loads(data)

        frame = packet["frame"]
        generator = packet["generator"]

        print("Received Frame:", frame)
        print("Generator:", generator)

        if verify(frame, generator):
            result = "Frame Accepted"
        else:
            result = "Frame Rejected"

        print(result)
        conn.sendall(result.encode())

    except (ValueError, KeyError, TypeError) as e:
        print("Invalid packet:", e)
        conn.sendall("Invalid Data".encode())

    finally:
        conn.close()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("CRC Server Started...")

while True:
    conn, addr = server.accept()

    threading.Thread(
        target=handle_client,
        args=(conn, addr)
    ).start()
