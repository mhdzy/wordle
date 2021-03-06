#!/usr/bin/env python3

import argparse
import sys

import message.Message
import player.AutoPlayer
import player.DailyPlayer
import player.InteractivePlayer


def main(argv):
    parser = argparse.ArgumentParser(
        description="daily wordle driver parser",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("-a", "--answer", help="Set the Wordle answer")
    parser.add_argument("-d", "--daily", help="Run daily game", action="store_true")
    parser.add_argument(
        "-i", "--interactive", help="Run an interactive game", action="store_true"
    )
    parser.add_argument(
        "-s", "--simulate", help="Run a simulation", action="store_true"
    )

    parser.add_argument(
        "-g",
        "--group",
        help="A flag to enable iMessage groups as recipients",
        action="store_true",
    )
    parser.add_argument(
        "-p",
        "--phone-number",
        help="A valid iPhone phone number or Group name"
    )

    args = parser.parse_args()
    config = vars(args)

    if config.get("daily"): 
        game = player.DailyPlayer.DailyPlayer()
        # if user also chose interactive, this will setup the target game obj
        config.update({'answer': game.game.game.answer})
    
    if config.get("interactive"):
        game = player.InteractivePlayer.InteractivePlayer()
    elif config.get("simulate"):
        game = player.AutoPlayer.AutoPlayer()

    if config.get("answer", None) is not None:
        game.set(config.get("answer"))

    game.play()

    def msg_wrapper(game, mode, config):
        messager = message.Message.Message(mode=mode)
        messager.send_message(
            phone_number=config.get("phone_number"),
            message=game.game.game.show_feedback(),
        )

    if config.get("phone_number") is not None:
        mode = "group" if config.get("group") else "phone"
        msg_wrapper(game=game, mode=mode, config=config)

    print(repr(game.game))

    return game.game


if __name__ == "__main__":
    main(sys.argv[1:])
