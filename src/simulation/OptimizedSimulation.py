#!/usr/bin/env python3

import math
import operator
import tqdm

import src.player.Player as Player
import src.simulation.OptimizedCache as OptimizedCache


class OptimizedSimulation:
    def __init__(self) -> None:
        self.cache = OptimizedCache.OptimizedCache()
        self.scores: list = []
        self.newgame()

        return None

    def __repr__(self) -> str:
        return f"OptimizedSimulation()"

    def __str__(self) -> str:
        return f"OptimizedSimulation()"

    def newgame(self):
        self.plr = Player.Player()
        self.tmpdf = self.cache.df
        return self

    def gsize(self, group: str):
        return self.tmpdf.groupby(group).size()

    def gnorm(self, fbcounts: list, size: int):
        return [f / size for f in fbcounts]

    def glog(self, vec: list, base=2):
        return [math.log(x, base) if x > 0 else 0 for x in vec]

    def ginvlog(self, vec: list, base=2):
        return self.glog([1 / x for x in vec], base=base)

    def gscore(self, word: str):
        px = self.gnorm(self.gsize(word), size=len(self.tmpdf))
        logpx = self.ginvlog(px)
        return sum([x * y for (x, y) in zip(px, logpx)])

    def autoguess(self):
        if self.plr.game.turn == 0:
            guess = "tares"
        else:
            guesses = {word: self.gscore(word) for word in list(self.tmpdf.index)}
            guess = max(guesses.items(), key=operator.itemgetter(1))[0]

        fbraw = self.plr.guess(guess)
        fbcode = self.cache.fb2int(self.cache.fbflat(fbraw))
        self.tmpdf = self.tmpdf[self.tmpdf[guess].isin([fbcode])]

    def simulate(self):
        self.newgame()
        while not self.plr.game.win and not self.plr.game.lose:
            self.autoguess()
        self.scores.append(0 if self.plr.game.lose else self.plr.game.turn)


class OptimizedSimulationDriver:
    def __init__(self) -> None:
        return None

    def simulate(self, ngames: int = 1):
        opt = OptimizedSimulation()
        for _ in tqdm.tqdm(range(ngames)):
            opt.simulate()
        return opt.scores
