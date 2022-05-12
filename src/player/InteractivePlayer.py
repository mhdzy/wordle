#!/usr/bin/env python3

import src.player.Player as Player


class InteractivePlayer:
    def __init__(self) -> None:
        self.game = Player.Player()
        return None

    def __str__(self) -> str:
        return f"InteractivePlayer(game: {str(self.game)})"

    def __repr__(self):
        return repr(self.game)
    
    def set(self, answer: str):
        self.game.game.answer = answer
        return self

    def play(self):
        while not self.game.game.win  and self.game.game.turn < 6:
            print(repr(self.game))
            move = input('> ')
            if move == 'hint' or move == 'help':
                print('hint: ' + self.game.generateguess())
            else:
                self.game.guess(move)

        self.game

        return self
