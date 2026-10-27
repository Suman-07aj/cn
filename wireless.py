import simpy
import random

def send(env, tech, src, dst, n, delay, loss, distance, reach):
    received = 0

    for i in range(1, n + 1):
        yield env.timeout(0.2)
        print(f"{env.now:.2f}s: {src} sends Packet {i} to {dst}")

        if distance > reach or random.random() < loss:
            print(f"Packet {i} LOST")
        else:
            yield env.timeout(delay)
            received += 1
            print(f"Packet {i} received by {dst}, delay={delay*1000:.0f} ms")

    print(f"\n{tech}: Sent={n}, Received={received}, Lost={n-received}")
    print(f"Delivery Ratio={received/n*100:.1f}%")

random.seed(1)
env = simpy.Environment()

env.process(send(env, "Wi-Fi", "W1", "W2", 5, 0.015, 0.02, 20, 100))
env.process(send(env, "Bluetooth", "B1", "B2", 5, 0.035, 0.05, 5, 10))
env.process(send(env, "Zigbee", "Z1", "Z2", 5, 0.075, 0.03, 20, 50))
env.process(send(env, "Bluetooth", "B1", "B3", 5, 0.035, 0.05, 25, 10))

env.run()