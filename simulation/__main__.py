#!/usr/bin/env python3

import collections
import numpy as np

import simulation.Simulator

max_games: int = 100
log_rate: float = 0.01

if __name__ == "__main__":
    player = simulation.Simulator.Simulator(
        **{"max_games": max_games, "log_rate": log_rate}
    )
    guesses = player.autoplay()

    # summarised view
    counted = collections.Counter(guesses)

    # save out raw list
    np.savetxt(
        fname="tests/data/simulation-test-new-simulator.csv",
        X=guesses,
        delimiter=",",
    )
