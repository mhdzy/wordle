#!/usr/bin/env python3

import argparse
import sys

import player.HumanPlayer
import player.AutoPlayer


def main(argv):
    parser = argparse.ArgumentParser(
        description="daily wordle driver parser",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("-a", "--answer", help="Wordle answer")
    parser.add_argument("-s", "--sim", help="Run a simulation", action="store_true")
    parser.add_argument("-u", "--human", help="Manual mode", action="store_true")
    args = parser.parse_args()
    config = vars(args)

    if config.get("human"):
        game = player.HumanPlayer.HumanPlayer()
    elif config.get("sim"):
        game = player.AutoPlayer.AutoPlayer()
    else:
        raise KeyError(
            "Missing game mode option: '-u' to play manually or '-s' to simulate."
        )

    if config.get("answer", None) is not None:
        game.set(config.get("answer"))

    game.play()

    print(repr(game.game))

    return game.game


if __name__ == "__main__":
    main(sys.argv[1:])
