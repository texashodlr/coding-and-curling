#!/bin/bash

# For loop
for f in *.txt; do
	echo "$f"
done

# Array
arr=(a b c)
echo ${arr[1]}

# Conditions
if [[ $x -gt 10 ]]; then echo "big"; fi

# Text processing
cat file.txt | grep "pattern"
awk '{print $1}' file.txt

# While loop
while read line; do echo $line; done < file.txt

