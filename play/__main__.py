
import game.PlayGame as pg
import json

game = pg.PlayGame()

part: int = 1
base: int = 2000

sim_list: list = game.fb_simulate(partition = part, base = base)
sim_dict: dict = {s: {k[0]: k[1] for k in sim_list[s]} for s in sim_list}

with open("data/first-move-simulation-new-" + part + ".json", "w") as fd:
    json.dump(sim_dict, fd, indent=2)
