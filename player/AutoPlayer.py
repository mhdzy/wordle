from statistics import mean
import game.PlayGame as pg


class AutoPlayer:
    def __init__(self) -> None:
        self.MAX_GAMES = 2
        self.LOG_RATE = 0.10
        self.games: list = []
        self.scores: list = []
        print(f"Games to Play: {self.MAX_GAMES}")
        print(f"Logging Rate: {self.LOG_RATE}")
        return None

    def autoplay(self) -> list:
        for i in range(0, self.MAX_GAMES):
            if not i % (self.MAX_GAMES * self.LOG_RATE):
                print(f"playing game {i}")

            fb = []
            game = pg.PlayGame()
            failure = False

            while not game.game.win:
                try:
                    #fb.append(game.autoguess())
                    potential_guesses = game.fb_simulate()
                    average_remainders = [
                        mean(potential_guesses[x].values())
                        for x in potential_guesses.keys()
                    ]
                    next_guess = list(potential_guesses)[average_remainders.index(min(average_remainders))]
                    fb.append(game.guess(next_guess))
                except Exception as e:
                    # when the candidate list is empty, an err is thrown
                    game.game.win = True
                    failure = True

            game

            if failure:
                self.scores.append(-1)
            else:
                self.scores.append(len(game.guesses))

            self.games.append(game)

        return self.scores
