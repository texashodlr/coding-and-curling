# Question 4: 
"""
You receive a time-ordered stream of tuples (timestamp_sec, host_id, error_code) representing infrastructure alerts. 
    To avoid alert storms, an alert should be suppressed 
    if the same (host_id, error_code) appeared in the last W seconds; otherwise, it should be emitted.



Write a function that takes the stream (as a list of tuples) 
    and a window W (int seconds) and returns the list of tuples that should be emitted in order.
    
Example input:
events = [
    (0,   "node-1", "GPU_OVERHEAT"),
    (3,   "node-1", "GPU_OVERHEAT"),
    (8,   "node-2", "DISK_FULL"),
    (10,  "node-1", "GPU_OVERHEAT"),
    (12,  "node-1", "MEM_LEAK"),
    (18,  "node-2", "DISK_FULL"),
]
W = 10

Example output:
[
    (0, "node-1", "GPU_OVERHEAT"),
    (8, "node-2", "DISK_FULL"),
    (12, "node-1", "MEM_LEAK"),
    (18, "node-2", "DISK_FULL"),
]

So we can ingest the stream and basically look at the Node and Error and hold it then check the next event timestamp, if that is not within W then print and shift to the next entry
    We could have a system where we're holding an item then add another 
    Would need to check the current jobs time stamp and then everything within range 
    held item
    Here's the item at T = 0, the next item is at T = 1 so we surpress that item.
"""

def alerts(events, W):
    if not W or not events:
        raise ValueError("Nothing present")
    emit = [] # Warnings to emit
    nodes = [] # All the unique affected nodes
    for i in range(len(events)):
        if events[i][1] not in nodes:
            nodes.append(events[i][1])
    print(nodes)        
    for n in nodes:
        print(n)
        for i in range(len(events)):
            print(events[i])
            if not emit and events[i][1] == n:
                print("\t\t\t\tFirst item added")
                emit.append(events[i])
                exit
            elif emit:
                if emit[-1][1] is not n:
                    print("\t\t\t\tFirst item added")
                    emit.append(events[i])
                    exit
                elif (emit [-1][1] and events[i][1]) == n:
                    print(f" Last item: {emit[-1]}")
                    if (emit[-1][0] + W) < events[i][0]:
                        emit.append(events[i])
                        exit
    return emit

from typing import List, Tuple, Any, Dict
Event = Tuple[int, str, str]

def dedupe_alerts(events, W):
    if W < 0:
        raise ValueError("W must be non-neg")
    if not events:
        return []
    
    last_emitted: Dict[Tuple[str, str], int] = {}
    emitted: List[Event] = []
    print(last_emitted)
    print(emitted)
    
    for ts, host, code in events:
        key = (host, code)
        if key not in last_emitted or ts - last_emitted[key] >= W:
            emitted.append((ts, host, code))
            last_emitted[key] = ts
    return emitted

if __name__ == '__main__':
    events = [
    (0,   "node-1", "GPU_OVERHEAT"),
    (3,   "node-1", "GPU_OVERHEAT"),
    (8,   "node-2", "DISK_FULL"),
    (10,  "node-1", "GPU_OVERHEAT"),
    (12,  "node-1", "MEM_LEAK"),
    (18,  "node-2", "DISK_FULL"),]
    W = 10
    print(dedupe_alerts(events, W))
    #print(f"Solution: {alerts(events, W)}")

"""
for i in range(len(events)):
        print(events[i])
        if i == 0:
            emit.append(events[i])
            #most_recent.add(events
            exit
        surpress_range = events[i][0]+W  # T = 0 + 10 <10> where the lock occurs
        for j in range(i, len(events)):
            print(f" i: {events[i]}, j: {events[j]}")
            if events[j][0] > surpress_range and events[j][1] == events[i][1]:
                emit.append(events[j])
"""