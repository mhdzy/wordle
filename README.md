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

### Interactive Mode (`-i`)

Play Wordle interactively with:

```sh
$ python3 -m src.player -i
```

Initialize a game with a specific answer with:

```sh
$ python3 -m src.player -i -a snake
```

### Autoplay (`-s`)
To autoplay the game using an autosolver, run:

```sh
$ python3 -m src.player -s
```

Specifying an answer to the autosolver is the same as with interactive mode, using the `-a` flag:

```sh
$ python3 -m src.player -s -a snake
```

### Daily Play (`-d`)
To solve the day's particular Wordle game automatically, run:

```sh
$ python3 -m src.player -d
```

To play the daily Wordle in interactive mode, run:

```sh
$ python3 -m src.player -d -i
```

## Simluation
The `simulation` module allows for running a large number of Wordle games to measure the performance of the autosolving algorithm. Scores are exported and processed in R.

### Traditional Simulation
Simulating many games of Wordle can be done by invoking the `simulation` module and passing the `-n` (number of games):

```sh
$ python3 -m src.simulation -n 100
```

### Optimized Simulation (`-o`)
Traditional simulation takes 10 seconds to run a game, wheras the optimized simulator can play 5 games per second. 

```sh
$ python3 -m src.simulation -o -n 100
```

### Multithreaded Simulation (`-m`)
Simulations are by default multithreaded, but optimized simulations are not. Multithreading can be enabled *only for optimized simulations* with the `-m` flag, defaulting to using `cpu_count / 2` processes. You can specify the number of processes in the thread pool with the `-t` flag. Performance will degrade when using more cores than are physically available on the CPU.

Run an optimized multithreaded simulation using 2 threads:

```sh
$ python3 -m src.simulation -o -n 100 -m -t 2
```

## Sharing Games (macOS) (`-p`)
Sending Wordle games to others is a popular activity, so this repo comes equipped with either individual or group iMessaging capabilities (macOS *only*). 

To share the results of your daily interactive Wordle run, use:

```sh
$ python3 -m src.player -d -i --phone-number="9874563210"
```

If you're sharing the results with an iMessage group, you will need to enable this with the `-g` flag, and use the group name instead of a phone number. Since sharing is supported by all run modes, we can send a simulated run with an answer we supply to a group:

```sh
$ python3 -m src.player -s -a "zebra" -g --phone_number="GroupName"
```

Note: sharing is *not* supported by the `simulation` module.

## Code

To use the Wordle game in a Python project, you can initialize a game with:

```py
import src.player.Player as Player

game = Player.Player()
```

Guesses can be made with:

```py
game.guess("zebra")
```

To display the game object, use:

```py
print(repr(game))
```
