import game.PlayGame as pg

game = pg.PlayGame()

possible_feedbacks = game.fb_combos()

while not game.game.win:
    game.autoguess()
game
