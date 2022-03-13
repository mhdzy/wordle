from itertools import compress
import re
import game.WordleGame as wg


class PlayGame:
    """
    generate a wordle game and allow guesses
    """

    # same master word list shared across all games
    choices: list = []

    def __init__(self) -> None:
        self.game = wg.WordleGame()
        self.choices = self.game.choices
        self.weighted_choices: list = [self.game.choices]
        # can compare these against self.game.guesses and self.game.feedbacks
        self.guesses: list = []
        self.feedbacks: list = []
        self.tables: list = []
        self.regexes: list = []

        return None

    def __str__(self) -> str:
        return f"PlayGame(game: {str(self.game)})"

    def __repr__(self) -> str:
        return self.game.__repr__()

    def autoguess(self) -> list:
        """
        Takes an automated guess attempt for the game. Currently chooses the
        first word in the guess stack.
        :return list: The results of a guess attempt, usually the guess feedback.
        """
        if not len(self.weighted_choices):
            raise NotImplementedError("game ran out of words to pick")
        return self.guess(self.weighted_choices[-1][0])

    def guess(self, word: str = "") -> list:
        """
        Performs a 'guess' attempt to the Wordle game, and receives feedback
        on the guess. This is parsed to filter the remaining candidate word list
        down, after which the guess feedback is returned.
        :param word: A guess string.
        :return list: The feedback for the guess.
        """
        self.feedbacks.append(self.game.guess(word))
        self.weighted_choices.append(self.filter(self.feedbacks[-1]))

        return self.feedbacks[-1]

    def filter(self, fb: list = []) -> list:
        """
        Calculates a feedback table to consider the relationship of the
        feedback letters. This table is used to filter the remaining list of
        valid guess choices and return them.
        :param fb: Feedback from a guess attempt.
        :return list: A list of remaining valid guesses.
        """
        self.tables.append(self.fb_table(fb))
        self.regexes.append(self.fb_regex(fb, self.tables[-1]))
        leftover = list(
            map(
                lambda r, w: True if len(re.findall(r, w)) else False,
                [self.regexes[-1]] * len(self.weighted_choices[-1]),
                self.weighted_choices[-1],
            )
        )
        return list(compress(self.weighted_choices[-1], leftover))

    def fb_table(self, fb: list = []) -> dict:
        """
        Derives a feedback table including letter count and duplication indications.
        :param fb: similarity of guess (accuracy) derived from the guess and answer
        """
        table = {"pos": [], "fb": [], "letter": [], "count": [], "duplicate": []}

        for pos, item in enumerate(fb):
            table["pos"].append(pos)
            table["fb"].append(item[1])
            table["letter"].append(item[0])
            table["count"].append(table["letter"].count(item))
            table["duplicate"].append(True if table["count"][-1] > 0 else False)
            # todo: implement 'has_green_dup'
            # todo: implement 'has_yellow_dup'
            # tood: implement 'has_black_dup'

        return table

    def fb_regex(self, fb: list = [], tbl: dict = {}) -> str:
        """
        Derives a regex string to match against valid words who satisfy the
        feedback. Uses the table to quickly determine count/duplication status.
        :param fb: results from the game's guess feedback
        :param tbl: results from self.fb_table()
        """

        alphabet = "abcdefghijklmnopqrstuvwxyz"
        pos_regex = {k: alphabet for k in range(0, 5)}

        fb_let = [k for (k, _) in fb]
        fb_let_struct = {
            "g": self.pos_let(mode=2, values=fb),
            "y": self.pos_let(mode=1, values=fb),
            "b": self.pos_let(mode=0, values=fb),
        }

        for pos, item in enumerate(fb):
            tmp = {k: tbl[k][pos] for k in tbl.keys()}
            if tmp["fb"] == 2:
                pos_regex[pos] = tmp["letter"]
            elif tmp["fb"] == 1:
                pos_regex[pos] = pos_regex[pos].replace(tmp["letter"], "")
            elif tmp["fb"] == 0:
                if tmp["duplicate"]:
                    if tmp["letter"] in fb_let_struct["y"]:
                        # if has yellow duplicate, remove from current position
                        pos_regex[pos] = pos_regex[pos].replace(tmp["letter"], "")
                    elif tmp["letter"] in fb_let_struct["g"]:
                        # elif has green duplicate, remove from all but green duplicate positions
                        # get duplicate green indices of this letter
                        ignore_idx = list(
                            compress(
                                list(range(0, len(fb))),
                                [x == tmp["letter"] for x in fb_let],
                            )
                        )
                        # construct index of 0-4 excluding green indices
                        remove_idx = [
                            x for x in list(range(0, len(fb))) if x not in ignore_idx
                        ]
                        # remove at those indices
                        for pos2 in remove_idx:
                            pos_regex[pos2] = pos_regex[pos2].replace(tmp["letter"], "")
                else:
                    # if not duplicated, remove from all positions
                    for i, _ in enumerate(fb):
                        pos_regex[i] = pos_regex[i].replace(tmp["letter"], "")

        return "[" + "]+[".join(pos_regex.values()) + "]+"

    def pos_let(self, mode: int, values: list = []) -> list:
        """
        Finds the letters in the response who belong to each category.
        :param mode: an integer mode representing 'g' (2), 'y' (1), or 'b' (0)
        :param values: a list of tuples representing (letter, fb_int_code)
        """
        return list(
            compress([x[0] for x in values], list(map(lambda x: x[1] == mode, values)))
        )

    def pos_idx(self, mode: int, values: list = []) -> list:
        """
        Finds the index of the letters (in a base reference word) that correspond
        to each of the categories.
        :param mode: an integer mode representing 'g' (2), 'y' (1), or 'b' (0)
        :param values: a list of tuples representing (letter, fb_int_code)"""
        return list(
            compress(
                list(range(0, len(values))),
                list(map(lambda x: x == mode, values)),
            )
        )
