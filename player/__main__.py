#!/usr/bin/env python3

import argparse
import sys

import simulation.AutoPlayer as ap
import player.DailyPlayer as dp


def main(argv):
    parser = argparse.ArgumentParser(
        description="daily wordle driver parser",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument('-a', '--answer', help="Wordle game answer")
    args = parser.parse_args()
    config = vars(args)
    
    game = dp.DailyPlayer()
    game.set(config.get('answer')).play()

    print(repr(game.game))

    return game.game


if __name__ == "__main__":
    main(sys.argv[1:])
