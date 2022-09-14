#!/usr/bin/env python3

from bs4 import BeautifulSoup
import datetime
import re
import requests

import src.player.Player as Player


class DailyPlayer:

    url = "https://www.wmlcloud.com/games/what-is-todays-wordle-answer/"
    alt_url = "https://www.nme.com/guides/gaming-guides/heres-the-wordle-answer-for-today-3171240"
    alt2_url = "https://gdcbemina.com/nytimes-wordle-answer-today-june-12-2022-check-358-solution-and-hints/"

    def __init__(self, rewind: int = 0) -> None:
        self.game = Player.Player()
        self.game.game.answer = self.get_answer(rewind)

        return None

    def __str__(self) -> str:
        return (
            f"DailyPlayer(game: {str(self.game)}, answer: {str(self.game.game.answer)})"
        )

    def __repr__(self):
        return repr(self.game)

    def get_answers(self) -> list:
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, "html.parser")

        futurelist = soup.select("ul li strong")[-1]
        answerlist = soup.select("article ul li")

        # regex lookahead requires fixed-length expression, so we need to
        # handle variable length date digits and var-length month strings
        re_date = str(len(str(datetime.date.today().day)))
        re_month = str(
            len(
                datetime.datetime.strptime(
                    str(datetime.date.today().month), "%m"
                ).strftime("%B")
            )
        )

        re_str = (
            r"(?<=Wordle No\. [0-9]{3} \([\w]{"
            + rf"{re_month}"
            + r"} [0-9]{"
            + rf"{re_date}"
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

        # sometimes this is broken
        answer = re.findall(r"(?<=<strong>)[\w]{5}", str(futurelist))[0].lower()
        if answer == "wordl":
            answer = re.findall(re_str, str(futurelist))[0].lower()

        answers.insert(0, answer)

        return answers

    def get_answer(self, num: int = 0) -> str:
        return self.get_answers()[num]

    def set(self, answer: str):
        self.game.game.answer = answer
        return self

    def play(self):
        self.game.autoplay()
        return self
