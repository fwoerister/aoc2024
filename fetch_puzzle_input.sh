#!/bin/sh

day=`expr $(date +"%d")`
year=`expr $(date +"%Y")`

printf -v fday "%02d" $day

cookies="session=$SESSION"
target="https://adventofcode.com/$year/day/$day/input"


curl --cookie "$cookies" $target > "input/day$fday.txt"