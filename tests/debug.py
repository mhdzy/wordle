import game.PlayGame as pg
import json

game = pg.PlayGame()

#game.autoguess()
sim_list = game.simulate()
sim_dict = { s: { k[0]: k[1] for k in sim_list[s] } for s in sim_list }

with open("data/first-move-simulation.json", "w") as fd:
    json.dump(sim_dict, fd, indent=2)


if False:
    import game.PlayGame as pg

    game = pg.PlayGame()

    game.game.answer = "oxide"
    game.answer = game.game.answer
    game.guess("trail")
    game.guess("coves")
    game.guess("poise")
    game.guess("chime")
    game

    game.feedbacks.append([("t", 0), ("r", 0), ("a", 0), ("i", 1), ("l", 0)])
    game.remainder.append(game.filter(game.feedbacks[-1], game.remainder[-1]))
    game.feedbacks.append([("c", 0), ("o", 1), ("v", 0), ("e", 1), ("s", 0)])
    game.remainder.append(game.filter(game.feedbacks[-1], game.remainder[-1]))
    game.feedbacks.append([("p", 0), ("o", 1), ("i", 2), ("s", 1), ("e", 2)])
    game.remainder.append(game.filter(game.feedbacks[-1], game.remainder[-1]))
    game.feedbacks.append([("c", 0), ("h", 0), ("i", 2), ("m", 0), ("e", 2)])
    game.remainder.append(game.filter(game.feedbacks[-1], game.remainder[-1]))
    game.remainder[-1]

    game.feedbacks.append([("o", 0), ("u", 0), ("i", 0), ("j", 0), ("a", 1)])
    game.remainder.append(game.filter(game.feedbacks[-1], game.remainder[-1]))
    game.feedbacks.append([("w", 0), ("a", 1), ("l", 1), ("t", 1), ("z", 0)])
    game.remainder.append(game.filter(game.feedbacks[-1], game.remainder[-1]))
    game.feedbacks.append([("a", 1), ("l", 2), ("e", 0), ("r", 0), ("t", 2)])
    game.remainder.append(game.filter(game.feedbacks[-1], game.remainder[-1]))
    list(map(len, game.remainder))
