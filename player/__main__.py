from collections import Counter
import numpy as np

import player.AutoPlayer as ap

if __name__ == "__main__":
    player = ap.AutoPlayer()
    guesses = player.autoplay()

    # summarised view
    counted = Counter(guesses)

    # save out raw list
    np.savetxt(
        fname="data/test_10k.csv",
        X=guesses,
        delimiter=",",
    )
