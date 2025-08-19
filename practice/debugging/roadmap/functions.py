language = "Python"
print(id(language))
# Unique ID of the functions

numbers = [1,2,3,4,5]
len(numbers)

"""
def function_block([parameters]):
    <block>

"""

def calculate_cost(item, quantity, price):
    print(f"{quantity} {item} cost ${quantity * price:.2f}")

# Positional
calculate_cost("Banana", 20, 1.00)

# Keyword
calculate_cost(item="Banana", quantity=20, price=0.99)

# And you can mix keyword and positional
# But must always only follow keyword after positional

# Functions that affect global values are side effect inducing

numbers1 = [1, 2, 3, 4, 5, 6]

def double_num(numbers):
    for i, _ in enumerate(numbers):
        numbers[i] *=2

def double_num_2(numbers):
    result = []
    for number in numbers:
        result.append(number*2)
    return result

# List comprehension
def double_num_3(numbers):
    return [number*2 for number in numbers]

double_num(numbers1)

print(numbers1)
# No side effect call
double_num_2(numbers1)

print(numbers1)

def as_dict():
    return dict(one=1, two=2, three=3)

print(as_dict()["one"])


from pathlib import Path

def read_file_contents(file_path):
    path = Path(file_path)

    if not path.exists():
        print(f"Error: The file '{file_path}' does not exist.")
        return
    if not path.is_file():
        print(f"Error: '{file_path}' is not a file.")
        return
    return path.read_text(encoding="utf-8")

read_file_contents(file_path="file.log")

# Generator Iterators (use yield), memory eff. items on demand

def cumulative_average(numbers):
    total = 0
    for items, number in enumerate(numbers,1):
        total += number
        yield total/items

values = [1,2,3,4,5,6]

for cum_average in cumulative_average(values):
    print(f"Cumulative Average: {cum_average:.2f}")

# Closure
def closure_func():
    value = 42
    def closure():
        print(f"the value is {value}!")
    return closure

reveal_number = closure_func()
reveal_number()

# Arbitrary number of positional args
def variable_func(*args):
    print(args)

variable_func(1,3,4,4,5)

# Variable number of keyword args
def kw_func(**kwargs):
    print(kwargs)

kw_func(one=1, two=2, three=3)

def report(**kwargs):
    print("Report: ")
    for key, value in kwargs.items():
        print(f" - {key.capitalize()}: {value}")

report(name="Keyboard", price=19.99, quantity=5, category="PC Components")

# Combining positional and KW
"""
def func(*args, **kwargs):
"""

def average(*args):
    """Calculate the average of given numbers.

    Args:
        *args (float or int): One or more numeric values.

    Returns:
        float: The arithmetic mean of the provided values.

    Raises:
        ZeroDivisionError: If no arguments are provided.

    Examples:
        >>> average(10, 20, 30)
        20.0
        >>> average(5, 15)
        10.0
        >>> average(7)
        7.0
    """
    return sum(args) / len(args)

print(average.__doc__)

import asyncio

async def get_number1():
    return 42

#print(get_number1())

print(asyncio.run(get_number1()))

async def fetch_data():
    print("Fetching data from the server...")
    await asyncio.sleep(1)  # Simulate network delay
    print("Data received!")
    return {"user": "john", "status": "active"}

async def main():
    data = await fetch_data()
    print(f"Rx'd data: {data}")

asyncio.run(main())

# Built in functions: https://docs.python.org/3/library/functions.html