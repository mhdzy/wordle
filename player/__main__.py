#!/usr/bin/env python3

import argparse
import sys

import player.AutoPlayer
import player.DailyPlayer
import player.HumanPlayer


def main(argv):
    parser = argparse.ArgumentParser(
        description="daily wordle driver parser",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("-a", "--answer", help="Set the Wordle answer")
    parser.add_argument("-d", "--daily", help="Run daily game", action="store_true")
    parser.add_argument(
        "-s", "--simulate", help="Run a simulation", action="store_true"
    )
    parser.add_argument(
        "-i", "--interactive", help="Run an interactive game", action="store_true"
    )
    args = parser.parse_args()
    config = vars(args)

    if config.get("daily"):
        game = player.DailyPlayer.DailyPlayer()
    elif config.get("human"):
        game = player.HumanPlayer.HumanPlayer()
    elif config.get("simulate"):
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
