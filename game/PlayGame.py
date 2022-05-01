from itertools import compress
import math
import random
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
        self.remainder: list = [self.game.choices]
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
        Takes an automated guess attempt for the game. Currently chooses a
        random word from the guess stack. While the chosen word has been
        guessed, a new word is chosen.
        :return list: The results of a guess attempt, usually the guess feedback.
        """
        if not len(self.remainder[-1]):
            raise Exception("game ran out of words to pick")

        def generate_guess(pool):
            return pool[random.randint(0, len(pool) - 1)]

        while True:
            guess = generate_guess(self.remainder[-1])
            if guess not in self.guesses:
                break
            else:
                print(f"duplicate guess generated: {guess}")

        return self.guess(guess)

    def guess(self, word: str = "") -> list:
        """
        Performs a 'guess' attempt to the Wordle game, and receives feedback
        on the guess. This is parsed to filter the remaining candidate word list
        down, after which the guess feedback is returned.
        :param word: A guess string.
        :return list: The feedback for the guess.
        """

        self.guesses.append(word)
        self.feedbacks.append(self.game.guess(word))
        self.remainder.append(self.filter(self.feedbacks[-1], self.remainder[-1]))

        # remove the guess from potential future guess pools to avoid duplicates
        if word in self.remainder[-1]:
            self.remainder[-1].remove(word)

        return self.feedbacks[-1]

    def filter(self, fb: list = [], words: list = [], util: bool = False) -> list:
        """
        Trims down the list of remaining valid guesses given a particular
        feedback. Useful for computing arbitrary leftover words for any given
        feedback and word list.
        :param fb: Feedback from a guess attempt.
        :param words: A list of words to filter on.
        :param util: A flag to append regex filter & table to class variables.
        :return list: A list of remaining valid guesses.
        """
        # this flag avoids appending parsed input results to object variables
        # this behavior is useful when legitimately guessing, but not when
        # computing possible outcomes for all remaining valid guesses
        if not util:
            self.tables.append(self.fb_table(fb))
            self.regexes.append(self.fb_regex(fb, self.tables[-1]))
            regex = self.regexes[-1]
        else:
            regex = self.fb_regex(fb, self.fb_table(fb))

        leftover = list(
            compress(
                words,
                list(
                    map(
                        lambda r, w: True if len(re.findall(r, w)) else False,
                        [regex] * len(words),
                        words,
                    )
                ),
            )
        )
        return leftover

    def fb_table(self, fb: list = []) -> dict:
        """
        Derives a feedback table including letter count and duplication indications.
        :param fb: similarity of guess (accuracy) derived from the guess and answer
        """
        table = {"pos": [], "fb": [], "letter": [], "count": [], "duplicate": []}

        for pos, item in enumerate(fb):
            table["pos"].append(pos % self.game.word_length)
            table["fb"].append(item[1])
            table["letter"].append(item[0])
            table["count"].append(table["letter"].count(item[0]))
            table["duplicate"].append(True if table["count"][-1] > 1 else False)
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
        pos_regex = {k: alphabet for k in range(0, self.game.word_length)}

        fb_let = [k for (k, _) in fb]
        fb_let_struct = {
            "g": self.pos_let(mode=2, values=fb),
            "y": self.pos_let(mode=1, values=fb),
            "b": self.pos_let(mode=0, values=fb),
        }

        for pos, item in enumerate(fb):
            # lets us pass over the regex string multiple times
            pos = pos % self.game.word_length

            tmp = {k: tbl[k][pos] for k in tbl.keys()}

            # this should be cleaned up...
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
                    for i in range(0, self.game.word_length):
                        pos_regex[i] = pos_regex[i].replace(tmp["letter"], "")

        # core regex unnamed capture group, 0 or 1 times for the elements & set
        # use non-greedy +? quantifier to match each letter (and group) strictly once
        main = "([" + "][".join(pos_regex.values()) + "])+?"

        # lookahead group to verify presence of yellow letters
        lookahead_pre = "(?=\w*["
        lookahead_post = "]+\w*)"
        lookahead_core = fb_let_struct["y"] if (len(fb_let_struct["y"])) else ["\w"]
        lookahead = list(
            map(
                lambda x: "{}{}{}".format(lookahead_pre, x, lookahead_post),
                lookahead_core,
            )
        )

        regex = "^" + "".join(lookahead) + main + "$"

        return regex

    def fb_combos(self, alphabet=["0", "1", "2"]) -> list:
        """
        :return list: A list of valid feedback combinations.
        """
        outputs: list = []

        def kLength(set, prefix, n, k):
            nonlocal outputs

            if k == 0:
                outputs.append(prefix)
                return

            for i in range(n):
                newPrefix = prefix + set[i]
                kLength(set, newPrefix, n, k - 1)

        kLength(alphabet, "", len(alphabet), self.game.word_length)

        return outputs

    def fb_stitch(self, fb: str, word: str) -> list:
        """
        :param fb: A string representing N digits of feedback.
        :param word: A word string to stitch together with the feedback.
        """
        if not len(fb) or not len(word) or len(fb) != len(word):
            raise Exception("no feedback or word string given")

        return [(v, int(k)) for (k, v) in zip(fb, word)]

    def fb_simulate(self, partition: int = 0, base: int = 10) -> dict:
        # for word w in remaining words:
        #   get all remaining words
        #   get all types of feedback
        #   for tmp_fb in feedbacks:
        #     fb_stitch(fb, words)
        #     filter(fb, words, util = True)
        wordcounts: dict = {}

        enumerable = self.remainder[-1]
        if partition:
            offset = math.ceil(len(self.remainder[-1])/base)
            enumerable = self.remainder[-1][((partition - 1) * offset):(partition * offset)]

        for pos, item in enumerate(enumerable):
            print(
                "parsing word #"
                + str(pos)
                + "/"
                + str(len(enumerable))
                + " ("
                + item
                + ")"
            )
            wordcounts[item] = []
            for f in self.fb_combos():
                wordcounts[item].append(
                    [
                        f,
                        len(
                            self.filter(
                                self.fb_stitch(f, item),
                                self.remainder[-1],
                                util=True,  # do not modify game variables
                            )
                        ),
                    ]
                )

        return wordcounts

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
