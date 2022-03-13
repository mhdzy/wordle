from collections import Counter
import numpy as np
import game.PlayGame as pg

MAX_ITER = 10000
LOG_RATE = 0.10
games = []
guesses = ["score"]

for i in range(0, MAX_ITER):
    if not i % (MAX_ITER * LOG_RATE):
        print(f"playing game {i}")
    game = pg.PlayGame()
    failure = False

    while not game.game.win:
        try:
            fb = game.autoguess()
        except:
            game.game.win = True
            failure = True

    if failure:
        guesses.append(-1)
    else:
        guesses.append(len(game.game.guesses))

    games.append(game)

# summarised view
counted = Counter(guesses)

# save out raw list
np.savetxt(
    fname="test_10k.csv",
    X=guesses,
    delimiter=",",  
)
