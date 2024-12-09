#!/bin/sh

day=$1
year=$(date +"%Y")

printf -v fday "%02d" "$day"

cookies="session=$SESSION"
target="https://adventofcode.com/$year/day/$day/input"


if test -f "input/day$fday.txt";
then
  echo "file already in input directory!"
else
  curl -s --cookie "$cookies" "$target" > "input/day$fday.txt"
fi