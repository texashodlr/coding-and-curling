# Question 1
#   Reverse an array: write a function that takes an array and returns the array in reversed order 
#   Example: reverse_array([1,2,3]) -> [3,2,1]

"""Solution"""
# Generate a random array of 1000 ints.
import random
import timeit
    #x = random.randint(0,1000)
    #print(x)
x = []
while len(x) < 1000:
    x.append(random.randint(0,1000))
    # print(len(x))
    # print(x)
# Now have a random array of unsorted stuff
def reverse_array(original_array):
    reverse_len = (len(original_array) - 1)
    reversed_original_array = []
    while reverse_len > -1:
        reversed_original_array.append(original_array[reverse_len])
        reverse_len -= 1
    return reversed_original_array

rev_array = reverse_array(x) #      --> 5288.247ms
print(len(rev_array))
print(rev_array[0:5])
print(x[995:1000])

def reverse_array2(original_array):
    return original_array[::-1]

rev_array = reverse_array2(x) #     --> 4812.435 ms
print(len(rev_array))
print(rev_array[0:5])
print(x[995:1000])

a = '''
import random
def reverse_array(original_array):
    reverse_len = (len(original_array) - 1)
    reversed_original_array = []
    while reverse_len > -1:
        reversed_original_array.append(original_array[reverse_len])
        reverse_len -= 1
    return reversed_original_array
x = []
while len(x) < 1000:
    x.append(random.randint(0,1000))
rev_array = reverse_array(x)
'''
t = timeit.timeit(a,number=10000) * 1e3
print(round(t,3),"ms")

b = '''
import random
def reverse_array2(original_array):
    return original_array[::-1]
x = []
while len(x) < 1000:
    x.append(random.randint(0,1000))
rev_array = reverse_array2(x)
'''
t2 = timeit.timeit(b,number=10000) * 1e3
print(round(t2,3),"ms")