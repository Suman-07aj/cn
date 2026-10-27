import simpy


env=simpy.Environment()
packet_store=simpy.Store(env)
ack_store=simpy.Store(env)

def sender(env,packet_store,ack_store):
    for i in range(5):
        packet=i
        print("Packet:",i,"is sent",env.now)
        yield packet_store.put(packet)
        yield env.timeout(1)
        ack=yield ack_store.get()
        print(ack," at ",env.now)



def receiver(env,packet_store,ack_store):
    while True:
        packet=yield packet_store.get()
        print("packet received",packet,"at ",env.now)
        yield ack_store.put("Ack")
        

env.process(sender(env,packet_store,ack_store))
env.process(receiver(env,packet_store,ack_store))
env.run(until=10)