# Dict as mutable collections of key:val pairs

config = { 'color': 'green',
'width': 42,
'height': 100,
'font': 'Helvetica',}
print(config)

print(globals())
"""
__name__:__main__/ __doc__:none / __package__none
"""

class Number:
    def __init__(self, value):
        self.value=value

print(Number(42).__dict__)

# NO duplicate keys
# my_dict = {key:val, ...}
# Tuples as keys
a_dict = {(1,1):"a", (1,2):"b", (1,3):"c", (1,4):"d"}

print(a_dict[(1,2)])

MLB_teams = dict(Colorado="Rockies", Houston="Astros")

# Manual key addition
person = {}
person["first_name"] = "John"

# For loop keys
squares = {}
for integer in range(1,10):
    squares[integer] = integer**2

print(squares)

# Comprehension
triples = {integer: integer**3 for integer in range(1,10)}
print(triples)

print(triples.get(2))
print(triples.values())
print(triples.keys())
print(triples.items())
squares.update(triples)
print(squares)

# in, not in, .pop .popitme

for num, triplet in squares.items():
    print(num,"**3 = ", triplet)

# In place sorting dict
class SortableDict(dict):
    def sort_by_keys(self, reverse=False):
        sorted_items = sorted(
            self.items(),
            key=lambda item: item[0],
            reverse=reverse
        )
        self.clear()
        self.update(sorted_items)
    
    def sort_by_values(self, reverse=False):
        sorted_items = sorted(
            self.items(),
            key=lambda item: item[1],
            reverse=reverse
        )
        self.clear()
        self.update(sorted_items)
    
students = SortableDict({
'Fiona': 95.6,
'Charlie': 92.3,
'Alice': 89.5,
'Ethan': 88.9,
'Diana': 84.7,
'Hannah': 81.2,
'Bob': 76.0,
'George': 73.4
}
)
print(students)
students.sort_by_keys(reverse=True)
print(students)
students.sort_by_values(reverse=True)
print(students)