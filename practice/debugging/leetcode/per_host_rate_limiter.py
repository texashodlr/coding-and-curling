# Question 6
"""

You’re given a time-ordered list of request events as tuples (timestamp_sec, host_id). 
Implement a rate limiter that emits a request only if fewer than R requests for the same host_id 
    have been emitted in the last W seconds (inclusive). Otherwise, the request is suppressed.
Write a function that takes the events, W (window in seconds), and R (max emits per window), 
    and returns the list of emitted events in order.


Input:
events = [
    (0,  "node-1"),
    (3,  "node-1"),
    (9,  "node-1"),
    (10, "node-1"),
    (12, "node-2"),
    (15, "node-1"),
]
W = 10
R = 2

Output:
[
    (0,  "node-1"),
    (3,  "node-1"),
    (10, "node-1"),
    (12, "node-2"),
    (15, "node-1"),
]

"""

def rate_limiter(events, W, R):
    if not events:
        return []
    if not W:
        return []
    if not R:
        return []
    
    starting_time = events[0][0]
    emit = []
    # need like a count
    host_wind = {}    
    for i in range(len(events)):
        
        if (starting_time+W) > events[i][0]:
            # can possibly add item
            if events[i][1] in host_wind:
                if host_wind[events[i][1]] < R:
                    host_wind[events[i][1]] += 1
                    emit.append(events[i])
            elif events[i][1] not in host_wind:
                host_wind[events[i][1]] = 1
                emit.append(events[i])
        elif (starting_time+W) <= events[i][0]:
            host_wind.clear()
            starting_time = events[i][0] # new time then add event
            host_wind[events[i][1]] = 1
            emit.append(events[i])
    
    return emit

def rate_limiter_v2(events, W, R):
    if not events:
        return []
    if not W:
        return []
    if not R:
        return []
    
    starting_time = events[0][0]
    emit = []
    # need like a count
    host_wind = {}
    for ts, host in events:
        lst = host_wind.get(host)
        print(f" Lst: {lst}")
        if lst is None:
            lst = []
            host_wind [host] = lst
        while lst and lst[0] <= ts - W:
            lst.pop(0)
        if len(lst) < R:
            emit.append((ts, host))
            lst.append(ts)
        
    print(host_wind)
    return emit

if __name__ == "__main__":
    events = [
    (0,  "node-1"),
    (3,  "node-1"),
    (9,  "node-1"),
    (10, "node-1"),
    (12, "node-2"),
    (15, "node-1"),]
    W = 10
    R = 2
    print(rate_limiter(events, W, R))
    print(rate_limiter_v2(events, W, R))