# Wordle

## Overview
`wordle` implements a Wordle game and autosolver capable of playing the game automatically. This is done by receiving and parsing Wordle-style feedback, tracking the remaining potential answers, and choosing the "next best guess" until the game is won or lost. 

You can also play by yourself (interactively), provide custom answers, simulate games, and even share game results with others (macOS only).

## Install
Clone the repository with:

```sh
$ git clone git@github.com:mhdzy/wordle.git
```

## Play

### Interactive Mode

Play Wordle interactively with:

```sh
$ python3 -m player -i
```

Initialize a game with a specific answer with:

```sh
$ python3 -m player -i -a snake
```

### Autoplay
To autoplay the game using an autosolver, run:

```sh
$ python3 -m player -s
```

This will run a game of Wordle and attempt to solve it using the internal algorithm. It can be quite slow when running on games with a large remainder of potential solutions.

Specifying an answer to the autosolver is the same as with manual play, using the `-a` flag:

```sh
$ python3 -m player -s -a midst
```

### Daily Play
To solve the day's particular Wordle game automatically, run:

```sh
$ python3 -m player -d
```

To play the daily Wordle in interactive mode, run:

```sh
$ python3 -m player -d -i
```

### Simulate Play
Simulating many games of Wordle can be done with invoking the `simulation` module, and passing the `-n` (number of games) and `-l` (logging frequency) flags:

```sh
$ python3 -m simulation -n 2 -l 0
```
This will autoplay 2 games of Wordle and perform *no* logging. Multiply the 
number of games by the logging frequency to determine how often a log message will appear.

## Sharing Games (macOS)
Sending Wordle games to others is a popular activity, so this repo comes equipped with either individual or group iMessaging capabilities (macOS *only*). 

To share the results of your daily interactive Wordle run, use:

```sh
$ python3 -m player -d -i --phone-number="9874563210"
```

If you're sharing the results with an iMessage group, you will need to enable this with the `-g` flag, and use the group name instead of a phone number. Since sharing is supported by all run modes, we can send a simulated run with an answer we supply to a group:

```sh
$ python3 -m player -s -a "zebra" -g --phone_number="GroupName"
```

Note: sharing is *not* supported by the `simulation` module.

## Code

To use the Wordle game in a python project, you can initialize a `game` object by:

```py
import player.Player

game = player.Player.Player()
```

Guesses can be made with:

```py
game.guess("zebra")
```

To display the game object, use:

```py
repr(game)
```
