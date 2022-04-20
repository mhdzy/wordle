# Wordle

## Overview
`wordle` implements a Wordle game autosolver, capable of playing the game automatically. This is done by choosing a random guess from the sample word list, receiving and parsing wordle-style feedback, filtering the list to remaining candidate words, and looping until a solution is found.

## Play
Initialize a `game` object with `game.PlayGame.PlayGame()`. Subsequent guesses can be made with `game.guess()`. 

```py
import game.PlayGame as pg

game = pg.PlayGame()
```

To make a guess, run:

```py
game.guess("zebra")
```

To display the game (so far), use:

```py
game
```

## Autoplay
To autoplay the game, run:

```sh
$ python -m player
```

This will autoplay 10 games of Wordle and write the scores to `data/test.csv`. 

If you're interested, you can use the `pdb` module to inspect the games while they unfold.
