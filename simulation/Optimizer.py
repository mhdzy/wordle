#!/usr/bin/env python3

import pandas as pd
import multiprocessing
import os
import pickle
import tqdm

import game.Game
import game.Load
import player.Player


class Optimizer:

    df_path = "data/df.pkl"
    res_path = "data/res.pkl"

    def __init__(self):
        self.game = game.Game.Game()
        loader = game.Load.Load()
        self.words = list(set.union(set(loader.words), set(loader.answers)))
        self.words.sort()

        fbstr = player.Player.Player().combos()
        fbcode = list(range(len(fbstr)))
        self.fbmap = {k: v for (k, v) in zip(fbstr, fbcode)}
        self.invfbmap = {v: k for (k, v) in zip(fbstr, fbcode)}

        self.max_threads = int(multiprocessing.cpu_count() / 2)

        return None

    def __repr__(self) -> str:
        return "Optimizer"

    def __str__(self) -> str:
        return f"Optimizer()"

    def read_obj(file):
        return pickle.load(open(file, 'rb'))

    def write_obj(obj, file):
        pickle.dump(obj, open(file, 'wb'))

    def fbflat(self, fb: str = "") -> str:
        return "".join([str(v) for (k, v) in fb])

    def fb2int(self, fb: str = "") -> int:
        return self.fbmap.get(fb)

    def int2fb(self, fb: int = 0) -> str:
        return self.invfbmap.get(fb)

    def init_df(self, words: list = []) -> str:
        if os.path.exists(self.df_path):
            self.df = pd.read_pickle(self.df_path)
        else:
            ndarray = [[0] * len(words)] * len(words)
            self.df = pd.DataFrame(ndarray, words, words)
            self.df.to_pickle(self.df_path)
        return ""

    def init_res(self):
        if os.path.exists(self.res_path):
            self.res = pd.read_pickle(self.res_path)
        else:
            self.res = self.pop_df_mp()

    def insert_df(self, results):
        for idx in tqdm.tqdm(range(len(results))):
            self.df.iloc[idx, :] = self.res[idx][idx]
        # row name = guess; column name = answer
        self.df = self.df.transpose()

    def pop_df_serial(self) -> str:
        for i in range(len(self.words)):
            print(i)
            for j in range(len(self.words)):
                fb_tuple = self.game.calculate_feedback(self.words[i], self.words[j])
                fb_str = "".join([str(v) for k, v in fb_tuple])
                self.df.iloc[i, j] = self.fb2int(fb_str)
        return ""

    def pop_df_parallel(self, word) -> dict:
        dfrow = list(self.df.names.keys()).index(word)
        dfword = self.words[dfrow]
        print(f"processing #{dfrow} ({word})")
        result = [0] * len(self.words)
        for j in range(len(self.words)):
            fb_tuple = self.game.calculate_feedback(self.words[j], dfword)
            result[j] = self.fb2int("".join([str(v) for _, v in fb_tuple]))
        return {dfrow: result}

    def pop_df_mp(self) -> list:
        pool = multiprocessing.Pool(processes=self.max_threads)
        results = pool.map(self.pop_df_parallel, self.words)
        return results

    def opt_sim(self):
        def newgame():
          return player.Player.Player()
        
        game = newgame()