# Question 3
"""
You are monitoring disk usage (in GB) over time. 
Given a list of usage values and an integer k, 
	write a function that returns the maximum average disk usage observed over any k consecutive measurements.
IN:
    usage = [70, 72, 75, 90, 85, 100, 110, 95]
    k = 3
OUT:
    98.33...   # (100 + 110 + 95) / 3
    
So we're given a list and need to select the K highest items in the list then average them out and return.
Sort the list into ascending order and then go from there
"""


def window_avg(usage, k):
    if not k or not usage:
        raise ValueError("Missing entries")
    usage.sort()
    average = usage[-k:]
    print(average)
    sum = 0
    for num in average:
        sum += num
    return float((sum/k))    
    
def sliding_win_avg(usage, k):
    if not k or not usage:
        raise ValueError("Missing entries")
    list_avg = []
    for i in range(len(usage)):
        average = usage[(i+0):(i+k)]
        sum = 0
        for num in average:
            sum += num
        list_avg.append(sum/k)
    sum = 0
    #print(list_avg)
    for num in list_avg:
        sum += num
    return (sum/len(list_avg))
    
from typing import List

def max_avg_usage(usage: List[float], k: int) -> float:
    if k <= 0 or k > len(usage):
        raise ValueError("k must be between 1 and len(usage)")

    window_sum = sum(usage[:k])
    max_sum = window_sum

    for i in range(k, len(usage)):
        window_sum += usage[i] - usage[i - k]
        if window_sum > max_sum:
            max_sum = window_sum

    return max_sum / k
        
    
if __name__ == '__main__':
    k = 3
    usage = [70, 72, 75, 90, 85, 100, 110, 95]
    print(f"V1: {window_avg(usage, k)}")
    print(f"V2: {sliding_win_avg(usage, k)}")
    print(f"V3: {max_avg_usage(usage,k)}")    