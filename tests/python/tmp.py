#!/usr/bin/env python3

import player.Player as pl

game = pl.Player()
game.game.answer = 'undid'
game.guess('tares')
game.guess('zebra')
game.guess('quack')
game.guess('pilum')

vals = game.generateguesses()