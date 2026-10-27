import simpy
import random
import math

def simulate(algo, data_kb, seg_kb, bandwidth, rtt_ms, loss_pct):
    env = simpy.Environment()

    total = math.ceil(data_kb / seg_kb)
    remaining = total
    cwnd = 1.0
    ssthresh = 16
    wmax = 1.0
    btlbw = 1.0
    retrans = 0
    lost_total = 0
    rounds = 0
    total_acked = 0
    min_rtt = rtt_ms / 1000

    loss = loss_pct / 100
    rtt = rtt_ms / 1000
    history = []

    def sender():
        nonlocal remaining, cwnd, ssthresh, wmax
        nonlocal btlbw, retrans, lost_total, rounds
        nonlocal total_acked, min_rtt

        while remaining > 0 and rounds < 20000:
            rounds += 1
            sent = min(remaining, max(1, int(cwnd)))

            # Simulate packet loss
            lost = sum(random.random() < loss for _ in range(sent))
            acked = sent - lost

            retrans += lost
            lost_total += lost
            total_acked += acked
            remaining -= acked

            # Estimate RTT and bandwidth
            tx_time = sent * seg_kb * 8 / (bandwidth * 1000)
            used_rtt = max(rtt, tx_time)
            yield env.timeout(used_rtt)
            min_rtt = min(min_rtt, used_rtt)
            btlbw = max(btlbw, acked / used_rtt)

            # Update congestion window
            if algo == "Reno":
                if lost:
                    ssthresh = max(2, cwnd / 2)
                    cwnd = ssthresh
                elif cwnd < ssthresh:
                    cwnd += acked
                else:
                    cwnd += 1

            elif algo == "CUBIC":
                if lost:
                    wmax = cwnd
                    cwnd = max(1, cwnd * 0.7)
                else:
                    cwnd = max(cwnd + 1, wmax + 0.4 * rounds ** 3 / 100)

            else:  # Simplified BBR
                if rounds <= 6 and not lost:
                    cwnd *= 2
                else:
                    cwnd = max(4, btlbw * min_rtt * 2 * 1000)
                    if lost:
                        cwnd *= 0.85

            cwnd = max(1, cwnd)
            history.append((rounds, cwnd, used_rtt * 1000))

    env.process(sender())
    env.run()

    elapsed = env.now
    throughput = total * seg_kb * 8 / (elapsed * 1000) if elapsed else 0

    return {
        "Algorithm": algo,
        "Rounds": rounds,
        "Acknowledged": total_acked,
        "Lost": lost_total,
        "Retransmissions": retrans,
        "Avg RTT (ms)": round(
            sum(x[2] for x in history) / len(history), 2
        ) if history else 0,
        "Throughput (Mbps)": round(throughput, 2),
        "Completion Time (s)": round(elapsed, 3),
        "Final cwnd": round(cwnd, 2)
    }


# Input validation
while True:
    try:
        data = float(input("Data size (KB): "))
        seg = float(input("Segment size (KB): "))
        bw = float(input("Bandwidth (Mbps): "))
        rtt = float(input("Base RTT (ms): "))
        loss = float(input("Packet loss (%): "))

        if min(data, seg, bw, rtt) <= 0:
            print("Data, segment size, bandwidth and RTT must be positive!")
        elif not 0 <= loss <= 100:
            print("Loss must be between 0 and 100!")
        else:
            break

    except ValueError:
        print("Enter valid numeric values!")

# Compare all three algorithms under identical conditions
for algo in ["Reno", "CUBIC", "BBR"]:
    random.seed(42)
    result = simulate(algo, data, seg, bw, rtt, loss)
    print("\n", result)
