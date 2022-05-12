#!/usr/bin/env python3

import src.player.Player as Player


class AutoPlayer:

    def __init__(self, **kwargs: dict) -> None:
        self.game = Player.Player()
        return None
    
    def __str__(self) -> str:
        return f"AutoPlayer(game: {str(self.game)})"

    def __repr__(self):
        return repr(self.game)

    def set(self, answer: str):
        self.game.game.answer = answer
        return self

    def play(self):
        while not self.game.game.win and self.game.game.turn < 6:
            self.game.autoguess()

        self.game

        return self

    def reset(self):
        self.game = Player.Player()
        return self
