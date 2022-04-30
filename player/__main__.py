from collections import Counter
import numpy as np

import player.AutoPlayer as ap

if __name__ == "__main__":
    player = ap.AutoPlayer(**{'max_games': 2, 'log_rate': 0.01})
    guesses = player.autoplay()

    # summarised view
    counted = Counter(guesses)

    # save out raw list
    np.savetxt(
        fname="data/test-new-name.csv",
        X=guesses,
        delimiter=",",
    )
