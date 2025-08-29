# Q5: Top-K Frequent Hosts
"""
You are given a list of log entries as tuples (timestamp, host_id). Each entry represents one request handled by that host.

Write a function that, given the logs and an integer k, returns the top-k hosts by number of requests handled. 
If two hosts tie, order them by host_id alphabetically


 IN######
logs = [
    (1, "node-1"),
    (2, "node-2"),
    (3, "node-1"),
    (4, "node-3"),
    (5, "node-2"),
    (6, "node-1"),
]
k = 2
OUT########
["node-1", "node-2"]


"""

def top_k_hosts(logs, k):
    if not k:
        raise ValueError("K is inval")
    if not logs:
        raise ValueError("Logs are inval")
    all_hosts  = [logs[i][1] for i in range(len(logs))]
    print(all_hosts.sort())
    unique_hosts = set([logs[i][1] for i in range(len(logs))])
    print(f" All: {all_hosts}, Unique: {unique_hosts}")
    k_count = {}
    for host in unique_hosts:
        k_count[host] = all_hosts.count(host)
    print(k_count)
    
def top_k_hosts_v2(logs, k):
    if not k:
        raise ValueError("K is inval")
    if not logs:
        raise ValueError("Logs are inval")
    all_hosts  = list([logs[i][1] for i in range(len(logs))])
    sorted_all_hosts = all_hosts
    sorted_all_hosts.sort()
    unique_hosts = set(sorted_all_hosts)
    #print(f" Sorted: {sorted_all_hosts}, Unique: {unique_hosts}")
    k_count = []
    for host in unique_hosts:
        k_count.append((host, sorted_all_hosts.count(host)))
    res = sorted(k_count, key=lambda x: x[1])
    res.reverse()
    #print(res)
    return res[:k]

from collections import Counter
def top_k_hosts_speed(logs, k):
    if k <= 0:
        return []
    if not logs:
        return []
    counts = Counter(host for _, host in logs)
    ranked = sorted(counts.items(), key=lambda it: (-it[1], it[0]))
    return [host for host, _ in ranked[:k]]

if __name__ == "__main__":
    logs = [
    (1, "node-3"),
    (2, "node-2"),
    (3, "node-1"),
    (4, "node-3"),
    (5, "node-1"),
    (6, "node-1"),]
    k = 2
    print(top_k_hosts_v2(logs,k))
    print(top_k_hosts_speed(logs,k))
        