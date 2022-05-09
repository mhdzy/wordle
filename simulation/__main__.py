#!/usr/bin/env python3

import argparse
import numpy as np
import sys
import yaml

import simulation.Simulator

config_file = "simulation/config.yaml"

def read_yaml(file):
    with open(file, "r") as f:
        return yaml.safe_load(f)

def main(argv):
    parser = argparse.ArgumentParser(
        description="daily wordle driver parser",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("-n", "--max_games", help="Number of games to simulate")
    parser.add_argument("-l", "--log_rate", help="Inverse log frequency")

    args = vars(parser.parse_args())
    dargs = read_yaml(config_file)

    player = simulation.Simulator.Simulator(
        **{
            # pull from command-line args first, fallback to config
            "max_games": int(args.get("max_games", dargs.get("max_games"))),
            "log_rate": float(args.get("log_rate", dargs.get("log_rate"))),
        }
    )
    guesses = player.autoplay()

    # save out raw list
    np.savetxt(
        fname="tests/data/simulation-test-new-simulator.csv",
        X=guesses,
        delimiter=",",
    )


if __name__ == "__main__":
    main(sys.argv[1:])
