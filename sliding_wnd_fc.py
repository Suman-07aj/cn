
import simpy

def sender(env, buffer, n, size, rate, delay, st):
    for i in range(1, n + 1):

        # Wait until receiver has enough buffer space
        while buffer.level + size > buffer.capacity:
            if not st['waiting']:
                print("Sender Waiting - Buffer Full")
                st['waiting'] = True
            yield env.timeout(0.01)

        st['waiting'] = False

        # Send segment and reserve buffer space
        yield buffer.put(size)
        st['tx'] += 1
        print("Segment", i, "Transmitted")

        # Transmission and network delay
        yield env.timeout(size / rate + delay)

        st['rx'] += 1
        st['ack'] += 1
        rwnd = buffer.capacity - buffer.level
        print("ACK Received:", i, "| rwnd:", round(rwnd, 2), "KB")


def receiver(env, buffer, rate, st):
    while True:
        if buffer.level > 0:
            amount = min(1, buffer.level)
            yield env.timeout(amount / rate)
            yield buffer.get(amount)
            st['processed'] += amount
            print("Processing Data | Buffer:",
                  round(buffer.level, 2), "KB")
        else:
            yield env.timeout(0.01)


# Input with validation
while True:
    try:
        data = float(input("Total data (KB): "))
        size = float(input("Segment size (KB): "))
        buf = float(input("Receiver buffer (KB): "))
        send_rate = float(input("Sender rate (KB/s): "))
        recv_rate = float(input("Receiver rate (KB/s): "))
        delay = float(input("Network delay (ms): ")) / 1000

        if min(data, size, buf, send_rate, recv_rate) <= 0:
            print("Values must be positive!")
        elif size > buf:
            print("Segment size cannot exceed buffer size!")
        elif data < size:
            print("Total data must be at least one segment!")
        else:
            break

    except ValueError:
        print("Enter valid numeric values!")

n = int(data // size)
if data % size != 0:
    n += 1

st = {'tx': 0, 'rx': 0, 'ack': 0,
      'processed': 0, 'waiting': False}

env = simpy.Environment()
buffer = simpy.Container(env, capacity=buf, init=0)

env.process(receiver(env, buffer, recv_rate, st))
env.process(sender(env, buffer, n, size, send_rate, delay, st))

env.run()

total_time = env.now
throughput = data / total_time if total_time > 0 else 0

print("\n--- TCP FLOW CONTROL SUMMARY ---")
print("Segments Generated:", n)
print("Segments Transmitted:", st['tx'])
print("Segments Received:", st['rx'])
print("ACKs:", st['ack'])
print("Data Processed:", round(st['processed'], 2), "KB")
print("Total Time:", round(total_time, 2), "s")
print("Throughput:", round(throughput, 2), "KB/s")
print("Final Buffer Occupancy:", round(buffer.level, 2), "KB")
print("Final rwnd:", round(buf - buffer.level, 2), "KB")

