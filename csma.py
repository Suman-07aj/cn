import simpy
import random

def node(env, name, channel, stats):
    cwmin, cwmax = 4, 16
    for i in range(5):
        yield env.timeout(random.uniform(0.01, 0.05))
        attempts = 0
        while attempts < 4:
            backoff = random.randint(0, cwmin - 1)
            print(f"{name}: Packet {i+1}, Backoff={backoff}")

            yield env.timeout(backoff * 0.001)

            if not channel.triggered:
                channel.succeed(name)
                print(f"{name}: Transmitting")
                yield env.timeout(0.01)
                print(f"{name}: Success")
                stats["success"] += 1
                channel = env.event()
                break
            else:
                print(f"{name}: Collision/Channel Busy")
                stats["collisions"] += 1
                attempts += 1
                cwmin = min(cwmin * 2, cwmax)
                stats["retrans"] += 1

def run(env):
    channel = env.event()
    stats = {"success": 0, "collisions": 0, "retrans": 0}

    for i in range(5):
        env.process(node(env, f"N{i+1}", channel, stats))

    yield env.timeout(1)
    print("\nSuccessful:", stats["success"])
    print("Collisions:", stats["collisions"])
    print("Retransmissions:", stats["retrans"])

env = simpy.Environment()
env.process(run(env))
env.run()