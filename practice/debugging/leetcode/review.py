
# Example of a sliding window problem

def longest_unique_substring(s):
    seen = {}
    left = 0
    maxlen = 0
    for right, ch in enumerate(s):
        if ch in seen and seen[ch] >= left:
            left = seen[ch] +1
        seen[ch] = right
        maxlen = max(maxlen, right - left + 1)
    return maxlen

s_string = "sadasdasdasdasdasd"
print(longest_unique_substring(s_string))

# Stack is a list with append() and pop()
# Queue dequeue with append() and popleft()

def is_valid(s):
    stack = []
    pairs = {')':'(',']':'[', '}':'{'}
    for ch in s:
        if ch in pairs.values():
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
    return not stack

def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        if target - num in seen:
            return [seen[target-num], i]
        seen[num] = i

def binary_search(nums, target):
    l, r = 0, len(nums)-1
    while l <= r:
        m = (l+r)//2
        if nums[m] == target: return m
        if nums[m] < target: l = m+1
        else: r = m-1
    return -1

nums = [1,2,3,4,5,8]
print(binary_search(nums, 8))
