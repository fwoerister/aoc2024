import os
from requests import post
from datetime import datetime

SESSION_ID = os.environ['SESSION']
YEAR = datetime.today().year
DAY = datetime.today().day


def submit_answer(answer, day=DAY, level=1, year=YEAR):
    url = f"https://adventofcode.com/{year}/day/{day}/answer"
    data = {
        "level": f"{level}",
        "answer": f"{answer}",
    }
    response = post(url, data=data, cookies={'session': SESSION_ID})

    return response.text.find("That's not the right answer") == -1
