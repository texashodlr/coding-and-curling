number = 1
if number > 5:
    raise Exception(f"The number should not exceed 5.({number=})")
print(number)

number = 1
assert (number < 5), f"The number should not exceed 5. ({number=})"
print(number)

# python3 -O exceptions.py

def linux_interaction():
    import sys
    if "linux" in sys.platform:
        raise RuntimeError("Function cannot run on Linux systems.")
    print("Doing Windows things.")

try:
    linux_interaction()
except RuntimeError as error:
    print(error)
    print("Windows function wasn't executed!")
    #pass

try:
    with open("file.log") as file:
        read_data = file.read()
except FileNotFoundError as fnf_error:
    print("Couldn't open file.log")
else:
    print("Doing even more windows things.")

try:
    linux_interaction()
except RuntimeError as error:
    print(error)
else:
    try:
        with open("file.log") as file:
            read_data = file.read()
    except FileNotFoundError as fnf_error:
        print("Couldn't open file.log")
finally:
    print("No more errors encountered continue to press!") 

class PlatformException(Exception):
    """In compatible platform."""

def linux_interaction_2():
    import sys
    if "linux" in sys.platform:
        raise PlatformException("Function is being run on a linux box")
    print("Doing linux things.")

linux_interaction_2()

try: 
    linux_interaction_2()
except PlatformException as error:
    print(error)