#!/bin/bash
read -p "enter the circles radius " radius
pi=3.14159
area=$(echo "$pi * ($radius * $radius)" | bc -l)
echo $area
