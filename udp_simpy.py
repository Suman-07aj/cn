
import simpy
import random

def sender(env, ch, n, interval, loss, dmin, dmax, st):
    for i in range(1, n + 1):
        yield env.timeout(interval)
        gen = env.now
        st['gen'] += 1

        print("Packet", i, "Generated")

        if random.random() < loss:
            print("Packet", i, "Lost")
            continue

        st['tx'] += 1
        delay = random.uniform(dmin, dmax)
        env.process(deliver(env, ch, i, gen, delay))


def deliver(env, ch, seq, gen, delay):
    yield env.timeout(delay)
    yield ch.put((seq, gen))


def receiver(env, ch, st):
    while True:
        seq, gen = yield ch.get()
        d = env.now - gen

        st['rx'].append(seq)
        st['delay'].append(d)

        print("Packet", seq, "Received | Delay:",
              round(d * 1000, 2), "ms")


# Input validation
while True:
    try:
        n = int(input("Number of packets: "))
        interval = float(input("Generation interval (ms): "))
        loss = float(input("Packet loss (%): "))
        dmin = float(input("Minimum delay (ms): "))
        dmax = float(input("Maximum delay (ms): "))

        if n <= 0 or interval <= 0:
            print("Packet count and interval must be positive!")
        elif not 0 <= loss <= 100:
            print("Packet loss must be between 0 and 100!")
        elif dmin < 0 or dmax < dmin:
            print("Invalid delay range!")
        else:
            break

    except ValueError:
        print("Enter valid numeric values!")

# Convert milliseconds to seconds
interval /= 1000
loss /= 100
dmin /= 1000
dmax /= 1000

st = {'gen': 0, 'tx': 0, 'rx': [], 'delay': []}
env = simpy.Environment()
ch = simpy.Store(env)

env.process(sender(env, ch, n, interval, loss, dmin, dmax, st))
env.process(receiver(env, ch, st))
env.run()

rx = len(st['rx'])
lost = n - rx
delays = st['delay']

print("\n--- UDP SUMMARY ---")
print("Generated:", st['gen'])
print("Transmitted:", st['tx'])
print("Received:", rx)
print("Lost:", lost)
print("Missing packets:", sorted(set(range(1, n + 1)) - set(st['rx'])))
print("PDR:", round(rx / n * 100, 2), "%")
print("PLR:", round(lost / n * 100, 2), "%")
print("Min delay:", round(min(delays) * 1000, 2) if delays else 0, "ms")
print("Max delay:", round(max(delays) * 1000, 2) if delays else 0, "ms")
print("Avg delay:", round(sum(delays) / len(delays) * 1000, 2) if delays else 0, "ms")
