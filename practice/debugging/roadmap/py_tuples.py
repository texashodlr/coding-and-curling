# Tuples are also immutable

red = (255, 0 , 0)
print(red)

record = ("John", 35, "Python Developer")
print(record)
print(record[0])

# Single item tuple
single_tuple = (42,)
print(single_tuple)
A = tuple([1,2,3,4])
print(A)
A = tuple("Bananan")
print(A)

plane = tuple({"manufacturer": "Boeing", "model": "747", "passengers": 416,}.values())
print(plane)
# tuple(start:stop:step)

monthly_incomes = (("January", 5000),
                   ("February", 5500),
                    ("March", 6000),
                    ("April", 5800),
                    ("May", 6200),
                    ("June", 7000),
                    ("July", 7500),
                    ("August", 7300),
                    ("September", 6800),
                    ("October", 6500),
                    ("November", 6000),
                    ("December", 5500)
                    )
print(monthly_incomes)
total_income = 0
for income in monthly_incomes:
    total_income += income[1]
print(total_income)

quarter_income=0
for index, (month,income) in enumerate(monthly_incomes, start=1):
    print(f"{month:>10}: {income}")
    quarter_income += income
    if index % 3 == 0:
        print(f"-"*20)
        print(f"{'Quarter':>10}: {quarter_income}", end="\n\n")
        quarter_income = 0

numbers = ("2", "9", "5", "1", "6")
print(tuple([int(number) for number in numbers]))

print(numbers.count("9"))
print(numbers.index("9"))

print("9" not in numbers)
print(len(monthly_incomes))

from collections import namedtuple
Person = namedtuple("Person", "name age position")
print(Person)
person1 = Person("John", 35, "Gamer")
print(person1.name)
print(person1.age)
print(person1.position)

from typing import NamedTuple

class Employee(NamedTuple):
    name: str
    age: int
    position: str = "Python Developer"

import csv

with open("employees.csv", mode="r") as csv_file:
    reader = csv.reader(csv_file)
    next(reader) # Skipping headers
    employees = []
    for name, age, position in reader:
        employees.append(Employee(name, int(age), position))

print(employees)

from dataclasses import dataclass
@dataclass
class Employee2:
    name: str
    age: int
    position: str = "Python Developer"

with open("employees.csv", mode="r") as csv_file:
    reader = csv.reader(csv_file)
    next(reader) # Skipping headers
    employees = []
    for name, age, position in reader:
        employees.append(Employee2(name, int(age), position))

print(employees)