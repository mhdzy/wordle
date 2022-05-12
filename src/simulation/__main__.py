#!/usr/bin/env python3

import argparse
import multiprocessing
import numpy as np
import sys
import yaml

import src.logger.Logger as Logger
import src.simulation.OptimizedSimulation as OptimizedSimulation
import src.simulation.Simulation as Simulation


def read_yaml(file):
    with open(file, "r") as f:
        return yaml.safe_load(f)


def write_csv(obj, file):
    np.savetxt(
        fname=file,
        X=obj,
        delimiter=",",
    )


def main(argv):
    config_file = "src/simulation/config.yaml"
    output_path = "tests/data/"

    logger = Logger.Logger().create().get()

    parser = argparse.ArgumentParser(
        description="Wordle Simulation parser",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("-l", "--log_rate", help="Inverse log frequency")
    parser.add_argument("-n", "--max_games", help="Number of games to simulate")
    parser.add_argument(
        "-o", "--optimize", help="Run the optimized simulation", action="store_true"
    )
    parser.add_argument(
        "-m", "--multithread", help="Multithread the simulation", action="store_true"
    )
    parser.add_argument(
        "-t", "--threads", help="Choose the number of threads. Only works with '-m'."
    )

    args = vars(parser.parse_args())
    dargs = read_yaml(config_file)

    if args.get("threads") is not None:
        max_threads = min(multiprocessing.cpu_count(), int(args.get("threads")))
    else:
        max_threads = int(multiprocessing.cpu_count() / 2)

    ngames = int(args.get("max_games", dargs.get("max_games")))
    mpgames = [int(ngames / max_threads) for _ in range(max_threads)]
    if args.get("optimize"):
        logger.debug("optimized simulation")
        sim = OptimizedSimulation.OptimizedSimulationDriver()
        output_path += f"simulation-optimized-{ngames}.csv"
    else:
        logger.debug("regular simulation")
        sim = Simulation.SimulationDriver()
        output_path += f"simulation-{ngames}.csv"

    if args.get("multithread"):
        logger.debug(f"multithreading is using {max_threads} threads")
        pool = multiprocessing.Pool(processes=max_threads)
        result = pool.map(sim.simulate, mpgames)
    else:
        logger.debug("multithreading is disabled")
        result = sim.simulate(ngames)
    write_csv(obj=result, file=output_path)


if __name__ == "__main__":
    main(sys.argv[1:])
