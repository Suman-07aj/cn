
import socket
import json
from crc import encode_data

HOST = "127.0.0.1"
PORT = 5001

data = input("Enter Data Frame: ")
generator = input("Enter Generator Polynomial: ")

if (not data or any(b not in "01" for b in data)
        or len(generator) < 2
        or generator[0] != "1"
        or any(b not in "01" for b in generator)):
    raise ValueError("Enter valid binary data and generator")

frame = encode_data(data, generator)
print("\nCRC Codeword:", frame)

print("\n1. No Error")
print("2. Single Bit Error")
print("3. Multiple Bit Error")
print("4. Burst Error")

choice = int(input("Choice: "))
send_frame = list(frame)


def flip_bit(position):
    send_frame[position] = (
        "1" if send_frame[position] == "0" else "0"
    )


if choice == 2:
    bit = int(input("Bit Position: "))
    flip_bit(bit)

elif choice == 3:
    n = int(input("Number of Bits: "))

    for i in range(n):
        bit = int(input(f"Bit Position {i + 1}: "))
        flip_bit(bit)

elif choice == 4:
    start = int(input("Burst Start Position: "))
    length = int(input("Burst Length: "))

    for bit in range(start, start + length):
        flip_bit(bit)

packet = {
    "frame": "".join(send_frame),
    "generator": generator
}

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

client.sendall(json.dumps(packet).encode())

print("\nServer Response:")
print(client.recv(1024).decode())

client.close()
