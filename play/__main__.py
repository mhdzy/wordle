import play.mpsim as mpsim

import json
import multiprocessing as mp

max_threads = int(mp.cpu_count())
ranges = [i + 1 for i in range(max_threads)]
pool = mp.Pool(processes=max_threads)

results = pool.map(mpsim.mpsim, ranges)

sim_list: list = {k: v for x in results for k, v in x.items()}
sim_dict: dict = {s: {k[0]: k[1] for k in sim_list[s]} for s in sim_list}

with open("data/first-move-simulation-new-mp.json", "w") as fd:
    json.dump(sim_dict, fd, indent=2)
