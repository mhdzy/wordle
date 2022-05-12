#!/usr/bin/env python3

import multiprocessing
import os
import pickle
import tqdm

import src.game.Game as Game
import src.game.Load as Load
import src.logger.Logger as Logger
import src.player.Player as Player


class OptimizedCache:
    df_path = "data/df.pkl"
    cache_path = "data/cache.pkl"

    # shared reference objects
    max_threads = int(multiprocessing.cpu_count() / 2)
    player = Player.Player()
    loader = Load.Load()
    logger = Logger.Logger().create().get()
    game = Game.Game()

    def __init__(self) -> None:
        self.words = list(set.union(set(self.loader.words), set(self.loader.answers)))
        self.words.sort()

        # feedback strings and integer codes
        fbstrs = self.player.combos()
        fbints = list(range(len(fbstrs)))
        self.fbmap = {k: v for (k, v) in zip(fbstrs, fbints)}
        self.invfbmap = {v: k for (k, v) in zip(fbstrs, fbints)}

        self.init_cache()
        self.init_df()

        return None

    def __repr__(self) -> str:
        return f"Optimizer()"

    def __str__(self) -> str:
        return f"Optimizer(max_threads = {self.max_threads})"

    def read_obj(self, file):
        return pickle.load(open(file, "rb"))

    def write_obj(self, obj, file):
        pickle.dump(obj, open(file, "wb"))

    def fbflat(self, fb: str = "") -> str:
        return "".join([str(v) for (k, v) in fb])

    def fb2int(self, fb: str = "") -> int:
        return self.fbmap.get(fb)

    def int2fb(self, fb: int = 0) -> str:
        return self.invfbmap.get(fb)

    def init_cache(self):
        if os.path.exists(self.cache_path):
            self.logger.debug("reading cache")
            self.cache = self.read_obj(self.cache_path)
        else:
            self.logger.debug("recreating cache")
            self.cache = self.calc_df_mp()
            self.write_obj(self.cache, self.cache_path)
        return self

    def init_df(self, words: list = []):
        if os.path.exists(self.df_path):
            self.logger.debug("reading df")
            self.df = self.read_obj(self.df_path)
        else:
            self.logger.debug("inserting into df")
            self.insert_df()
            self.write_obj(self.df, self.df_path)
        return self

    def calc_df(self, word) -> dict:
        result = [0] * len(self.words)
        j: int = list(self.df.names.keys()).index(word)
        print(f"processing #{j} ({word})")
        for i in range(len(self.words)):
            result[i] = self.fb2int(
                "".join(
                    [
                        str(v)
                        for _, v in self.game.calculate_feedback(
                            self.words[i], self.words[j]
                        )
                    ]
                )
            )
        return {j: result}

    def calc_df_mp(self) -> list:
        pool = multiprocessing.Pool(processes=self.max_threads)
        return pool.map(self.calc_df, self.words)

    def insert_df(self):
        for idx in tqdm.tqdm(range(len(self.cache))):
            self.df.iloc[idx, :] = self.cache[idx][idx]
        # row name = answer; column name = guess
        self.df = self.df.transpose()
