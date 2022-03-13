from collections import Counter
import numpy as np
import game.PlayGame as pg


class AutoPlayer:
    MAX_GAMES = 10000
    LOG_RATE = 0.10

    def __init__(self) -> None:
        self.games: list = []
        self.guesses: list = []
        return None

    def autoplay(self) -> list:
        for i in range(0, self.MAX_GAMES):
            if not i % (self.MAX_GAMES * self.LOG_RATE):
                print(f"playing game {i}")

            game = pg.PlayGame()
            failure = False

            while not game.game.win:
                try:
                    fb = game.autoguess()
                except:
                    # when the candidate list is empty, an err is thrown
                    game.game.win = True
                    failure = True

            if failure:
                self.guesses.append(-1)
            else:
                self.guesses.append(len(game.game.guesses))

            self.games.append(game)

        return self.guesses


if __name__ == "__main__":
    ap = AutoPlayer()
    guesses = ap.autoplay()

    # summarised view
    counted = Counter(guesses)

    # save out raw list
    np.savetxt(
        fname="data/test_10k.csv",
        X=guesses,
        delimiter=",",
    )
