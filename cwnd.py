import simpy
import random

def tcp_sender(env, algo, total, bandwidth, loss):
    cwnd = 1
    sent = 0
    start = env.now

    while sent < total:
        packets = min(int(cwnd), total - sent)
        for _ in range(packets):
            sent += 1
            if random.random() < loss:
                print(f"{env.now:.2f}s | Packet LOST")
                if algo == "Reno":
                    cwnd = max(1, cwnd / 2)
                elif algo == "CUBIC":
                    cwnd = max(1, cwnd * 0.7)
                else:
                    cwnd = max(1, cwnd)
            else:
                print(f"{env.now:.2f}s | ACK received")

        if algo == "Reno":
            cwnd *= 2 if cwnd < 16 else 1.1
        elif algo == "CUBIC":
            cwnd += 2
        else:
            cwnd = bandwidth * 0.02

        print(f"cwnd={cwnd:.2f}")
        yield env.timeout(0.02)

    elapsed = env.now - start
    print(f"Algorithm: {algo}")
    print(f"Packets sent: {sent}")
    print(f"Throughput: {sent / elapsed:.2f} packets/s")


algo = input("Algorithm (Reno/CUBIC/BBR): ").strip().capitalize()
total = int(input("Total packets: "))
bandwidth = float(input("Bandwidth (Mbps): "))
loss = float(input("Packet loss probability (0 to 1): "))

if algo not in ["Reno", "Cubic", "Bbr"]:
    raise ValueError("Choose Reno, CUBIC, or BBR")

random.seed(1)
env = simpy.Environment()
env.process(tcp_sender(env, algo, total, bandwidth, loss))
env.run()