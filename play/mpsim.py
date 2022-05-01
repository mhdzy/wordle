import game.PlayGame as pg

def parallel_wrapper(part: int = 0):
    game = pg.PlayGame()
    return game.fb_simulate(partition=part, base=12)