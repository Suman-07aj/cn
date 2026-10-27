import simpy

# --- Original Orthogonal Codes ---
c1 = [1, 1, 1, 1]
c2 = [1, -1, 1, -1]

# User Inputs
d1 = int(input("Enter data bit for client 1: "))
d2 = int(input("Enter data bit for client 2: "))

# Shared channel for summation
sum1 = []

def client1_sender(env):
    global c1_m
    c1_m = [1, 1, 1, 1]
    yield env.timeout(1)  # Simulates time taken by client 1
    if d1 == 0:
        c1_m = [-(x) for x in c1]

def client2_sender(env):
    global c2_m
    c2_m = [1, -1, 1, -1]
    yield env.timeout(1)  # Simulates time taken by client 2
    if d2 == 0:
        c2_m = [-(x) for x in c2]

def channel_and_receiver(env):
    yield env.timeout(2)  # Wait for both senders to complete
    
    print("Modulated codes:", c1_m, c2_m)
    
    # Summation on channel
    for x1, x2 in zip(c1_m, c2_m):
        sum1.append(x1 + x2)
    print("Combined Channel Signal (sum1):", sum1)

    # Demultiplexing
    t1 = 0
    t2 = 0
    for x1, x2 in zip(sum1, c1):
        t1 += (x1 * x2)
    for x1, x2 in zip(sum1, c2):
        t2 += (x1 * x2)

    print("t1:", t1)
    print("t2:", t2)

    # Decoding decision
    if t1 >= 0:
        print("data bit is 1 in client 1")
    elif t1 < 0:
        print("data bit is 0 in client 1")

    if t2 >= 0:
        print("data bit is 1 in client 2")
    else:
        print("data bit is 0 in client 2")

# Setup and run SimPy environment
env = simpy.Environment()
env.process(client1_sender(env))
env.process(client2_sender(env))
env.process(channel_and_receiver(env))

env.run()