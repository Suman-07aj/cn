import simpy
import ipaddress

def route(env, src, dst):
    path = [src]
    routers = {
        "192.168.1.0/24": ["R1"],
        "192.168.2.0/24": ["R1", "R2"],
        "192.168.3.0/24": ["R1", "R2", "R3"]
    }

    net = str(ipaddress.ip_network(dst + "/24", strict=False))
    if net not in routers:
        print(f"{src} -> {dst}: PACKET DROPPED (No route)")
        return

    for r in routers[net]:
        yield env.timeout(0.01)
        path.append(r)
        print(f"{env.now:.3f}s: Packet reached {r}")
        yield env.timeout(0.005)

    yield env.timeout(0.01)
    path.append(dst)
    print(f"{env.now:.3f}s: DELIVERED")
    print("Path:", " -> ".join(path))
    print("Hop count:", len(routers[net]))

env = simpy.Environment()

env.process(route(env, "PC2", "192.168.3.20"))
env.process(route(env, "PC1", "192.168.4.10"))

env.run()