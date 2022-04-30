import game.PlayGame as pg
import json

game = pg.PlayGame()

#game.autoguess()
sim_list = game.fb_simulate()
sim_dict = { s: { k[0]: k[1] for k in sim_list[s] } for s in sim_list }

with open("data/first-move-simulation-new.json", "w") as fd:
    json.dump(sim_dict, fd, indent=2)
