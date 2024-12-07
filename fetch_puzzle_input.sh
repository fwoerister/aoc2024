#!/bin/sh

day=$1
year=$(date +"%Y")

printf -v fday "%02d" "$day"

cookies="session=$SESSION"
target="https://adventofcode.com/$year/day/$day/input"

curl --cookie "$cookies" "$target" > "input/day$fday.txt"