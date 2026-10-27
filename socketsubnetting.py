import socket
import ipaddress

ip = input("Enter IP address: ")
mask = input("Enter subnet mask: ")

network = ipaddress.IPv4Network(ip + "/" + mask, strict=False)

print("Network Address:", network.network_address)
print("First Usable IP:", network.network_address + 1)
print("Last Usable IP:", network.broadcast_address - 1)
print("Broadcast Address:", network.broadcast_address)

print("IP in socket format:", socket.inet_aton(ip))