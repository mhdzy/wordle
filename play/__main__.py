import game.PlayGame as pg
import play.mpsim as mpsim
import json

from multiprocessing import Pool, cpu_count

pool = Pool(processes=int(cpu_count()))

all_ranges = [i + 1 for i in range(0, int(cpu_count()))]

results = pool.map(mpsim.parallel_wrapper, all_ranges)

part: int = 1
base: int = 2000
game = pg.PlayGame()

sim_list: list = game.fb_simulate(partition=part, base=base)
sim_dict: dict = {s: {k[0]: k[1] for k in sim_list[s]} for s in sim_list}

with open("data/first-move-simulation-new-" + part + ".json", "w") as fd:
    json.dump(sim_dict, fd, indent=2)
