#!/usr/bin/env python3

import time
import tqdm

import player.Player


class AutoPlayer:

    def __init__(self, **kwargs: dict) -> None:
        self.game = player.Player.Player()
        return None
    
    def __repr__(self):
        print(repr(self.game))
        return print(repr(self.game))

    def __str__(self) -> str:
        print(str(self.game))
        return str(self.game)

    def set(self, answer: str):
        self.game.game.answer = answer
        return self

    def play(self):
        # while not self.game.game.win and self.game.game.turn < 6:
        for _ in tqdm.tqdm(range(6)):
            self.game.autoguess()
            if self.game.game.win or self.game.game.lose:
                break

        self.game

        return self

    def reset(self):
        self.game = player.Player.Player()
        return self
