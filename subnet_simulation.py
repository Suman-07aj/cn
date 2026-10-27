import simpy
import ipaddress

env = simpy.Environment()

ip = input("Enter IP address: ")
mask = input("Enter subnet mask: ")

network = ipaddress.IPv4Network(ip + "/" + mask, strict=False)

def subnet(env):
    print("Network Address:", network.network_address)

    yield env.timeout(1)
    print("First Usable IP:", network.network_address + 1)

    yield env.timeout(1)
    print("Last Usable IP:", network.broadcast_address - 1)

    yield env.timeout(1)
    print("Broadcast Address:", network.broadcast_address)

env.process(subnet(env))
env.run()