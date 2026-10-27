
import simpy

env = simpy.Environment()
packet_store = simpy.Store(env)
ack_store = simpy.Store(env)

def sender(env, packet_store, ack_store):
    for i in range(5):
        packet = i
        ack_rcv = False

        while not ack_rcv:
            print("Packet", packet, "sent at", env.now)
            yield packet_store.put(packet)

            result = yield ack_store.get() | env.timeout(3)

            if ack_store.get in result:
                ack = result[ack_store.get]
                print(ack, "at", env.now)
                ack_rcv = True
            else:
                print("Timeout! Resending packet", packet, "at", env.now)

def receiver(env, packet_store, ack_store):
    received = set()

    while True:
        packet = yield packet_store.get()

        if packet == 2 and packet not in received:
            received.add(packet)
            yield env.timeout(5)

        print("Packet received:", packet, "at", env.now)
        yield ack_store.put("ACK for packet " + str(packet))

env.process(sender(env, packet_store, ack_store))
env.process(receiver(env, packet_store, ack_store))

env.run(until=30)
