import os
from datetime import datetime

from requests import post, get

SESSION_ID = os.environ['SESSION']
YEAR = datetime.today().year
DAY = datetime.today().day


def fetch_data(day=DAY, year=YEAR):
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    response = get(url, cookies={'session': SESSION_ID})

    with open(f"input/day{day}.input", "w") as input_file:
        input_file.writelines(response.text)


def submit_answer(answer, day=DAY, level=1, year=YEAR):
    url = f"https://adventofcode.com/{year}/day/{day}/answer"
    data = {
        "level": f"{level}",
        "answer": f"{answer}",
    }
    response = post(url, data=data, cookies={'session': SESSION_ID})

    return response.text.find("That's not the right answer") == -1


if __name__ == "__main__":
    fetch_data()
