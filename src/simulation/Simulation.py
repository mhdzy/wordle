#!/usr/bin/env python3

import tqdm

import src.player.Player as Player


class Simulation:
    def __init__(self) -> None:
        self.scores: list = []
        self.newgame()

        return None

    def __repr__(self) -> str:
        return f"Simulation()"

    def __str__(self) -> str:
        return f"Simulation()"

    def newgame(self):
        self.plr = Player.Player()
        return self

    def simulate(self) -> list:
        self.newgame()
        while not self.plr.game.win and not self.plr.game.lose:
            self.plr.autoguess()
        self.scores.append(self.plr.game.turn)

        return self.plr.game.turn


class SimulationDriver:
    def __init__(self) -> None:
        return None

    def simulate(self, ngames: int = 1):
        sim = Simulation()
        for _ in tqdm.tqdm(range(ngames)):
            sim.simulate()
        return sim.scores
