from statistics import mean
import game.PlayGame as pg


class AutoPlayer:

    def __init__(self, **kwargs: dict) -> None:
        self.max_games = kwargs.get('max_games', 10)
        self.log_rate = kwargs.get('log_rate', 0.10)
        self.games: list = []
        self.scores: list = []
        print(f"Games to Play: {self.max_games}")
        print(f"Logging Rate: {self.log_rate}")
        return None

    def autoplay(self) -> list:
        for i in range(0, self.max_games):
            if not i % (self.max_games * self.log_rate):
                print(f"playing game {i+1}")

            fb = []
            game = pg.PlayGame()
            failure = False

            while not game.game.win:
                try:
                    fb.append(game.autoguess())
                    if False:
                      # this code calculates the best next guess
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
