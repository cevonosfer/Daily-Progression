#!/bin/bash
array=(2 4 98 34 23 90 28)
sum=0
for number in "${array[*]}"; do
	(($sum += $number))
done

count=${#array[*]}
avg=$(echo "scale=2; $sum / $count" | bc)

echo "sum = $sum"
echo "average = $avg"
