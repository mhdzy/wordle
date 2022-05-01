from collections import Counter
import numpy as np

import player.AutoPlayer as ap

max_games: int = 100
log_rate: float = 0.01

if __name__ == "__main__":
    player = ap.AutoPlayer(**{"max_games": max_games, "log_rate": log_rate})
    guesses = player.autoplay()

    # summarised view
    counted = Counter(guesses)

    # save out raw list
    np.savetxt(
        fname="data/simulation-test-new-autoplayer.csv",
        X=guesses,
        delimiter=",",
    )
