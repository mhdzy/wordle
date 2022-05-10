#!/usr/bin/env python3

import itertools
import math
import multiprocessing
import random
import re

import game.Game


class Player:
    """
    Create a Wordle game and provide functions to guess, generate suitable
    guesses, automatically generate a word & guess, or auto-play either a
    single turn or multiple.

    Wraps the Game class guess function and extends the game with an
    autosolver. Uses class methods to generate feedback tables, regex filters
    and keep track of the game state, including all moves & remaining words.
    """

    # same master word list shared across all games
    choices: list = []

    def __init__(self) -> None:
        self.game = game.Game.Game()
        self.choices = self.game.choices
        self.remainder: list = [self.game.choices]
        # can compare these against self.game.guesses and self.game.feedbacks
        self.guesses: list = []
        self.feedbacks: list = []
        self.tables: list = []
        self.regexes: list = []

        # autoguess multithreading support
        self.max_threads: int = int(multiprocessing.cpu_count() / 2)
        self.max_remainder: int = 2000

        return None

    def __str__(self) -> str:
        return f"Player(game: {str(self.game)})"

    def __repr__(self) -> str:
        return repr(self.game)

    def generateguesses(self) -> str:
        """
        Generates a list of all possible guesses and their associated 'scores',
        as given by E[I(guess)] = sum {fb} (p(fb) * log(1/p(fb))).
        """
        results = self.simulate_mp()

        sim_list: list = {k: v for x in results for k, v in x.items()}
        sim_dict: dict = {k: [v[1] for v in sim_list[k]] for k in sim_list}

        # calculate p(x)
        flat_prob = {k: [x / len(sim_dict) for x in v] for k, v in sim_dict.items()}

        # calculate log(1/p(x))
        def log2inv(x: int = 0, base: float = math.e) -> float:
            return 0 if not x else math.log(1 / x, base)

        flat_log = {k: [log2inv(x, 2) for x in v] for k, v in flat_prob.items()}

        # multiply p(x) * log(1/p(x))
        exp_values = {
            k: [x * y for x, y in zip(flat_prob[k], flat_log[k])]
            for k in flat_prob.keys() & flat_log.keys()
        }

        # sum list for each word (alphabetical)
        sum_exp_values = {k: sum(v) for k, v in exp_values.items()}

        # sort list (reverse order, use [-1] key for highest score)
        sort_exp_values = {
            k: v for k, v in sorted(sum_exp_values.items(), key=lambda x: x[1])
        }

        # order the sorted expected value dict with largest at index 0
        # sort_exp_values_tuples = sorted(sum_exp_values.items(), key=lambda x: x[1])
        # sort_exp_values_tuples.reverse()
        # sort_exp_values = dict(collections.OrderedDict(sort_exp_values_tuples))
        # read_exp_values = {k: str(round(v, 2)) for k, v in sort_exp_values.items()}

        def duplicate(word: str = ""):
            return True if len(set(word)) == len(word) else False

        # find words with duplicated letters
        guess_words = list(sort_exp_values.keys())
        word_index = [
            pos for pos, item in enumerate(list(map(duplicate, guess_words))) if item
        ]

        # these are words without duplicate letters in them
        nonduplicated_exp_values = {
            k: v
            for k, v in sort_exp_values.items()
            if k in [guess_words[x] for x in word_index]
        }

        # if there aren't any 'nonduplicated' words left to use, we need to
        # pick from the duplicate bin
        guesslist = (
            nonduplicated_exp_values
            if len(nonduplicated_exp_values)
            else sort_exp_values
        )

        # return all words in raw form
        return guesslist

    def generateguess(self) -> str:
        """
        Generates a guess by simulating feedback results for the current game
        state. Chooses the word with the highest likelihood of maximally
        reducing the remaining word list 'score'.
        """

        # return the word with the highest score
        return list(self.generateguesses().keys())[-1]

    def randomguess(self) -> str:
        """
        Generates a random guess, chosen from the list of remaining words.
        """

        return self.remainder[-1][random.randint(0, len(self.remainder[-1]) - 1)]

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

    def autoguess(self) -> list:
        """
        Takes an automated guess attempt for the game. Currently chooses a
        random word from the guess stack. While the chosen word has been
        guessed, a new word is chosen.
        :return list: The results of a guess attempt, usually the guess feedback.
        """
        if not len(self.remainder[-1]):
            raise Exception("game ran out of words to pick")

        # print(f"{len(self.remainder[-1])}")

        # guess randomly on the first turn; it takes > 60 mins to run
        guess = (
            "tares"  # chosen from a list of precomputed words with the 'highest' score
            # self.randomguess()
            if not self.game.turn or len(self.remainder[-1]) > self.max_remainder
            else self.generateguess()
        )

        return self.guess(guess)

    def autoplay(self):
        """
        Automatically plays the game until a win or loss occurs.
        """
        while not self.game.lose and not self.game.win:
            self.autoguess()

        return self

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
            self.tables.append(self.table(fb))
            self.regexes.append(self.regex(fb, self.tables[-1]))
            regex = self.regexes[-1]
        else:
            regex = self.regex(fb, self.table(fb))

        return list(
            itertools.compress(
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

    def table(self, fb: list = []) -> dict:
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

    def struct(self, fb: list) -> list:
        """
        Finds the letters in the response who belong to each category.

        :param mode: an integer mode representing 'g' (2), 'y' (1), or 'b' (0)
        :param values: a list of tuples representing (letter, code)
        """

        def pletters(mode: int) -> list:
            return list(
                itertools.compress(
                    [x[0] for x in fb], list(map(lambda x: x[1] == mode, fb))
                )
            )

        return {
            k[0]: k[1]
            for k in list(zip(["g", "y", "b"], list(map(pletters, [2, 1, 0]))))
        }

    def regex(self, fb: list = [], tbl: dict = {}) -> str:
        """
        Derives a regex string to match against valid words who satisfy the
        feedback. Uses the table to quickly determine count/duplication status.

        :param fb: results from the game's guess feedback
        :param tbl: results from self.table()
        """

        alphabet = "abcdefghijklmnopqrstuvwxyz"
        regex = {k: alphabet for k in range(0, self.game.word_length)}

        struct = self.struct(fb)

        for pos, item in enumerate(fb):
            # lets us pass over the regex string multiple times
            pos = pos % self.game.word_length

            tmp = {k: tbl[k][pos] for k in tbl.keys()}

            # this should be cleaned up...
            if tmp["fb"] == 2:
                regex[pos] = tmp["letter"]
            elif tmp["fb"] == 1:
                regex[pos] = regex[pos].replace(tmp["letter"], "")
            elif tmp["fb"] == 0:
                if tmp["duplicate"]:
                    if tmp["letter"] in struct["y"]:
                        # if has yellow duplicate, remove from current position
                        regex[pos] = regex[pos].replace(tmp["letter"], "")
                    elif tmp["letter"] in struct["g"]:
                        # elif has green duplicate, remove from all but green duplicate positions
                        # get duplicate green indices of this letter
                        ignore_idx = list(
                            itertools.compress(
                                list(range(0, len(fb))),
                                [x == tmp["letter"] for x in [k for (k, _) in fb]],
                            )
                        )
                        # construct index of 0-4 excluding green indices
                        remove_idx = [
                            x for x in list(range(0, len(fb))) if x not in ignore_idx
                        ]
                        # remove at those indices
                        for pos2 in remove_idx:
                            regex[pos2] = regex[pos2].replace(tmp["letter"], "")
                else:
                    # if not duplicated, remove from all positions
                    for i in range(0, self.game.word_length):
                        regex[i] = regex[i].replace(tmp["letter"], "")

        # core regex unnamed capture group, 0 or 1 times for the elements & set
        # use non-greedy +? quantifier to match each letter (and group) strictly once
        main = "([" + "][".join(regex.values()) + "])+?"

        # lookahead group to verify presence of yellow letters
        lookahead_pre = "(?=\w*["
        lookahead_post = "]+\w*)"
        lookahead_core = struct["y"] if (len(struct["y"])) else ["\w"]
        lookahead = list(
            map(
                lambda x: "{}{}{}".format(lookahead_pre, x, lookahead_post),
                lookahead_core,
            )
        )

        regex = "^" + "".join(lookahead) + main + "$"

        return regex

    def combos(self, alphabet=["0", "1", "2"]) -> list:
        """
        Computes the possible combinations given an alphabet.

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

    def stitch(self, fb: str, word: str) -> list:
        """
        Stitches together a string of feedback with a word into a list.

        :param fb: A string representing N digits of feedback.
        :param word: A word string to stitch together with the feedback.
        """
        if not len(fb) or not len(word) or len(fb) != len(word):
            raise Exception("no feedback or word string given")

        return [(v, int(k)) for (k, v) in zip(fb, word)]

    def simulate(
        self, partition: int = 0, base: int = 10, verbose: bool = False
    ) -> dict:
        """
        Runs a simulation for all remaining words, calculating how long the
        resulting word list given every possible combination of words & feedback.

        :param partition: An integer indicating which partition to compute.
        :param base: An integer setting the number of partitions.
        :param verbose: A boolean flag to toggle extra output.
        """
        # for word w in remaining words:
        #   get all remaining words
        #   get all types of feedback
        #   for tmp_fb in feedbacks:
        #     stitch(fb, words)
        #     filter(fb, words, util = True)
        wordcounts: dict = {}

        if partition > base:
            print(
                f"partition {partition} is out of bounds (max {base}), defaulting to partition=0"
            )
            partition = 0

        enumerable = self.remainder[-1]
        if partition:
            offset = math.ceil(len(enumerable) / base)
            enumerable = enumerable[((partition - 1) * offset) : (partition * offset)]

        for pos, item in enumerate(enumerable):
            if verbose:
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
            for f in self.combos():
                wordcounts[item].append(
                    [
                        f,
                        len(
                            self.filter(
                                self.stitch(f, item),
                                self.remainder[-1],
                                util=True,  # do not modify game variables
                            )
                        ),
                    ]
                )

        return wordcounts

    def simulate_mp(self) -> list:
        """
        Parallelizes the class method simulate() by splitting the computation
        among self.max_threads processes. The resulting list is returned.
        """
        ranges = [i + 1 for i in range(self.max_threads)]

        pool = multiprocessing.Pool(processes=self.max_threads)
        results = pool.map(self.simulate, ranges)

        return results
