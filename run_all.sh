#!/bin/bash

days="1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25"

source .env
export SESSION=$SESSION

for day in $days
do
  printf -v fday "%02d" "$day"
  echo "##############"
  echo "# Run Day $fday #"
  echo "##############"

  ./fetch_puzzle_input.sh "$day"

  python "day$fday.py" "input/day$fday.txt"

  echo ""
done