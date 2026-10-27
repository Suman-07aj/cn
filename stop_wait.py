
import simpy

env = simpy.Environment()
packets = simpy.Store(env)
acks = simpy.Store(env)

def sender(env):
    for packet in range(5):
        acknowledged = False

        while not acknowledged:
            print("Sent packet", packet, "at", env.now)
            yield packets.put(packet)

            result = yield acks.get() | env.timeout(3)

            if acks.get in result:
                ack = result[acks.get]
                if ack == packet:
                    print("ACK received for", packet, "at", env.now)
                    acknowledged = True
                else:
                    print("Unexpected ACK:", ack, "at", env.now)
            else:
                print("Timeout! Resending", packet, "at", env.now)

def receiver(env):
    received = set()

    while True:
        packet = yield packets.get()

        if packet == 2 and packet not in received:
            received.add(packet)
            yield env.timeout(5)

        print("Received packet", packet, "at", env.now)
        yield acks.put(packet)

env.process(sender(env))
env.process(receiver(env))
env.run(until=40)
