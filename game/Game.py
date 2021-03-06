#!/usr/bin/env python3

import itertools
import datetime
import random

import game.Load


class Game:
    """
    generate a wordle game and allow guesses
    """

    # should be a global list that all objects share
    word_length: int = 5
    guess_limit: int = 6

    def __init__(self) -> None:
        self.win: bool = False
        self.lose: bool = False
        self.turn: int = 0
        self.answer: str = ""
        self.guesses: list = []
        self.feedbacks: list = []  # list of lists

        with game.Load.Load() as words:
            self.choices = words.answers + words.words
            self.answers = words.answers
            self.answer = self.answers[random.randrange(0, len(self.answers))]

            return None

    def __str__(self) -> str:
        return f"Game(win: {self.win}, turns: {self.turn}, answer: {self.answer}, guesses: {self.guesses}, feedback: {self.feedbacks})"

    def __repr__(self) -> str:
        fmt_str = "\n === Wordle Game === \n"

        fmt_str += (
            " [ ] game won\n"
            if not self.win
            else f" [x] game won\n" + f" answer: '{self.answer}'\n"
        )
        fmt_str += "\n"

        for idx in range(0, len(self.feedbacks)):
            fb = self.feedbacks[idx]

            fmt_str += " " + f"Turn {idx + 1}"
            fmt_str += " " + "".join([str(x[0]) for x in fb])
            fmt_str += " " + "".join([str(x[1]) for x in fb])
            fmt_str += "\n"

        fmt_str += " === === === === === \n\n"

        fmt_str += self.show_feedback() + "\n"

        return fmt_str

    def guess(self, word: str = ""):
        """
        Parses a submitted guess 'word'. Adds the word to the guess list,
        calculates feedback on the word with respect to the current answer,
        and appends the feedback to the feedback list. Returns the latest
        feedback.

        :param word: A 5 letter word guess.
        :return: Feedback on the guess.
        """

        if self.win:
            raise RuntimeError(f"The game has been won in {len(self.guesses)} guesses.")
        elif self.turn > 5:
            raise RuntimeError(f"The maximum number of guesses has been played.")
            pass

        if len(word) != 5:
            raise IndexError(f"Guess '{word}' does not have length 5.")

        if word not in self.choices:
            raise KeyError(f"Guess '{word}' was not found in the dictionary.")

        # make a guess
        self.turn += 1
        self.guesses.append(word)
        self.feedbacks.append(self.calculate_feedback(self.answer, word))

        # let the player know they won
        if word == self.answer:
            self.win = True
        elif self.turn > 6:
            self.lose = True

        # return latest feedback
        return self.feedbacks[-1]

    def apply_feedback(self, fb: list = [], vec: list = [], v: int = 0):
        """
        Positionally updates a list of feedback 'fb' with the value 'v'
        based on boolean values from the list 'vec'.
        """
        for k in range(len(vec)):
            if vec[k]:
                fb[k] = (fb[k][0], v)
        return fb

    def calculate_feedback(self, answer: str = "", word: str = "") -> dict:
        """
        Given a word, calculate the feedback.
        :param word: A 5 letter word guess to compare against the game answer.
        """
        if len(word) != 5:
            raise IndexError(f"Guess '{word}' does not have length 5.")

        # 'letterpool', keeps track of remaining 'valid' letters to score
        lp: list = list(answer)

        # tokenize the inputs to indexable components
        word: list = list(word)
        answer: list = list(answer)

        # enum { 'g': 2, 'y': 1, 'b': 0 }
        feedback: list = list(zip(word, [0] * len(word)))

        # setup empty structs to hold positions of each
        fb_green = [False] * len(word)
        fb_yellow = [False] * len(word)
        fb_black = [False] * len(word)

        # grab all matches as 'green'
        fb_green = [answer[k] == word[k] for k in range(len(answer))]
        green_idx = list(itertools.compress(list(range(0, len(answer))), fb_green))

        # update letterpool by removing green letters
        lp = list(itertools.compress(lp, [not i for i in fb_green]))

        # iterate over leftover words to determine
        for i in enumerate(word):
            (idx, letter) = i
            if idx in green_idx:
                pass
            elif letter in lp:
                lp.remove(letter)
                fb_yellow[idx] = True
            else:
                fb_black[idx] = True

        feedback = self.apply_feedback(feedback, fb_green, 2)
        feedback = self.apply_feedback(feedback, fb_yellow, 1)
        feedback = self.apply_feedback(feedback, fb_black, 0)

        return feedback

    def show_feedback(self, color: bool = True):
        """
        Shows feedback in 'color' mode using black/yellow/green emoji squares.
        :param color: A bool, when True displays emoji squares, when False uses integers.
        """

        colors = {0: "???", 1: "????", 2: "????"}

        fmt_date = datetime.date.today() - datetime.date(2021, 6, 19)

        fmt_score = "?"
        if self.turn < 6 and self.win:
            fmt_score = str(self.turn)
        elif self.turn >= 6:
            fmt_score = str(0)
        fmt_score += "/6"

        fmt_str = f"Wordle {fmt_date.days} {fmt_score}\n"
        for f in self.feedbacks:
            numeric_repr = [el[1] for el in f]
            emoji_repr = [colors[a] for a in numeric_repr]
            if color:
                fmt_str += "\n" + "".join(emoji_repr)
            else:
                fmt_str += "\n" + "".join([str(x) for x in numeric_repr])

        return fmt_str
