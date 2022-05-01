from statistics import mean
import game.PlayGame as pg

class DailyPlayer:
    def __init__(self, **kwargs: dict) -> None:
        self.game = pg.PlayGame()
        return None
    
    def set(self, answer: str):
        self.game.game.answer = answer
        return self

    def play(self):
        while not self.game.game.win and self.game.game.turn < 6:
            self.game.autoguess()

        self.game

        return self

    def reset(self):
        self.game = pg.PlayGame()
        return self