# Sets in python are mutable collection of unordered unique mutable elements
# List and dicts aren't allowed inside sets (mutability)
A = {1,2,4,6,8}
B = {1,2,3,4,5}

# Set union using .union()
print(A.union(B))
print(A | B)

# Set intersection
print(A.intersection(B))

print(A & B)

# Set difference
print(A.difference(B))
print(B.difference(A))

print (A - B)

# Symmetric difference
print(A.symmetric_difference(B))

A = {1,2,3,4,5}
B = {1,2,4}

print(A.issubset(B))
print(B.issubset(A))
print(A.issuperset(B))
print(1 in B)

S = set([1,10,100])
print(S)

S.add(2)
print(S)

S.remove(2)
print(S)
# Calling add multiple times does nothing as we're can only
#   have unique elements
#   Calling remove multiple times will raise 'KeyError'/s

Q = set()
Q.update(A)
print(Q)
Q.update(B)
print(Q)

S1 = {1,2,3}
S2 = S1.copy()
S1.clear()

S3 = {1, 2, 3, 4, 5, 6}
iter = 0
while iter is not 3:
    for number in S3:
        print(number)
    iter += 1

values = [1, 2, 3, 1, 2, 3, 1, 1, 2, 2, 3, 3]
unique_values = list(set(values))
print(unique_values)

all_clients = {104, 203, 255, 289, 448}
clients_bought_x = {104, 448}
clients_bought_y = {255, 104, 289}

print(clients_bought_x.difference(clients_bought_y))
print(clients_bought_y & clients_bought_x)
print(all_clients.difference(clients_bought_x) & all_clients.difference(clients_bought_y))