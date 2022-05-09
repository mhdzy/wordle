#!/usr/bin/env python3

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
        while not self.game.game.win and self.game.game.turn < 6:
            self.game.autoguess()

        self.game

        return self

    def reset(self):
        self.game = player.Player.Player()
        return self
