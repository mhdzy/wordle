# Wordle

## Overview
Implements a Wordle autosolver, capable of playing the game automatically. This is done by choosing a random guess from the sample word list, receiving feedback, filtering the list to remaining candidate words, and looping until a solution is found.

## Play
To play the game yourself, open the open the `play/__main__.py` file and run the code line by line. This will load a new Wordle game and attempt "zebra" as the first guess. Subsequent guesses can be made with `game.guess()`. 

## Autoplay
To autoplay the game, run:

```sh
$ python -m player
```

This will autoplay 10 games of Wordle and write the scores to `data/test.csv`. 

If you're interested, you can use the `pdb` module to inspect the games while they unfold.
