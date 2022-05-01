import game.PlayGame as pg

import multiprocessing as mp

def mpsim(partition: int = 0):
    return pg.PlayGame().fb_simulate(partition=partition, base=mp.cpu_count())
