"""
Storing data in python via four different modes:
1. List
2. Tuple
3. Set
4. Dict(ionary)

Set and dictionary are effectively hash-tables
"""

# Set elements are unique and cannot contain dupes
#   and remove dupes from a list
set_example = {1,1,2,3,3,3}
print(set_example)

# List and tuples are ordered seqs. of objects
# Tuple is immutable
# List and set are mutable
#   Sets we can only add items / not change
a_tuple = tuple(range(1000))
a_list = list(range(1000))
print(a_list.__sizeof__())
print(a_tuple.__sizeof__())

#Use list when:
    # Need to mutate the collection, when you need to remove/add new items to your collection of items
# Use tuple when:
#   If your data should/does not need to be changed
#   Tuples are faster than list (think for iteration)
#   Tuples as dict keys, list cannot because mutable (unhashable)
# Use Set which is hash table as its underlying data struct
#   Set is blazingly fast, looking in hash table is O(1)
#   If not storing dupes then set >>> list

# Speed check and iteration
# Courtesy of: https://stackoverflow.com/questions/2831212/python-sets-vs-lists/17945009#17945009
def iter_test(iterable):
    for i in iterable:
        pass

from timeit import timeit
# Set = 11.496
print(timeit("iter_test(iterable)",
       setup="from __main__ import iter_test; iterable = set(range(10000))",
       number=100000))
# List = 7.188
print(timeit("iter_test(iterable)",
       setup="from __main__ import iter_test; iterable = list(range(10000))",
       number=100000))
# Tuple = 6.7977
print(timeit("iter_test(iterable)",
       setup="from __main__ import iter_test; iterable = tuple(range(10000))",
       number=100000))

# Determining if an object is present
def in_test(iterable):
    for i in range(1000):
        if i in iterable:
            pass
# Set = 3.61561
print(timeit("in_test(iterable)",
             setup="from __main__ import in_test; iterable = set(range(1000))",
             number=100000))

# List = 219.959
print(timeit("in_test(iterable)",
             setup="from __main__ import in_test; iterable = list(range(1000))",
             number=100000))

# Tuple = 213.337
print(timeit("in_test(iterable)",
             setup="from __main__ import in_test; iterable = tuple(range(1000))",
             number=100000))

# Some minor pandas
import pandas as pd
color = ['blue', 'green', 'red', 'yellow']
fruit = ['blueberry', 'apple', 'cherry', 'banana']
df=pd.DataFrame(columns=['color','fruit'])
df['color'],df['fruit']=color,fruit

print(df)

name_tuple = ('Olivia', 'Nathan', 'Bethany', 'Jacob')
print(names_tuple)
print(type(names_tuple))

# Tuple types (4): empty/int/mixed/nested
# Indexing nested tuples:
n_tuple = ("kubernetes", "cloud native", [8, 6, 7, 5, 3, 0, 9])
#printing e in kubernetes
print(n_tuple[0][3])

tns_tuple = ('N', 'e', 'w', 'S', 't', 'a', 'c', 'k', 'R', 'o', 'k', 's')
print(tns_tuple.count('k'))
print(tns_tuple.index('k'))