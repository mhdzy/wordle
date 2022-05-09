#!/usr/bin/env python3

from bs4 import BeautifulSoup
import datetime
import re
import requests

import player.Player

class DailyPlayer:

    url = "https://www.wmlcloud.com/games/what-is-todays-wordle-answer/"

    def __init__(self) -> None:
        self.game = player.Player.Player()
        self.game.game.answer = self.get_answer()

        return None

    def __str__(self) -> str:
        return f"DailyPlayer(game: {str(self.game)}, answer: {str(self.game.game.answer)})"

    def __repr__(self):
        return repr(self.game)

    def get_answer(self, num: int = 0) -> str:
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, "html.parser")

        futurelist = soup.select("ul li strong")[-1]
        answerlist = soup.select("article ul li")

        # if date is two digits, we need to quantify the second [0-9] regex
        # with a {2}. otherwise we should use {1}
        re_date_rep = str(len(str(datetime.date.today().day)))
        re_month_rep = str(
            len(
                datetime.datetime.strptime(
                    str(datetime.date.today().month), "%m"
                ).strftime("%B")
            )
        )

        re_str = (
            r"(?<=Wordle No\. [0-9]{3} \([\w]{"
            + rf"{re_month_rep}"
            + r"} [0-9]{"
            + rf"{re_date_rep}"
            + r"}\): )"
            + r"([\w]{5}){1}"
        )

        answers = " ".join(
            [
                a[0].lower() if len(a) else ""
                for a in [
                    re.findall(re_str, str(x).replace("\xa0", "")) for x in answerlist
                ]
            ]
        ).split()

        answer = re.findall(r"(?<=<strong>)[\w]{5}", str(futurelist))[0].lower()

        # return answers[0]
        return answer

    def play(self):
        self.game.autoplay()

        return self