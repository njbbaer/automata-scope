import numpy as np
from collections import namedtuple

from seed import *

class RuleList():
    def __init__(self, rule_list):
        self.rule_list = rule_list
        self.rule_index = 0
        self.seed_index = 0
        self.print_state()

    def current_rule(self):
        return self.rule_list[self.rule_index]

    def current_seed(self):
        return self.current_rule().seeds[self.seed_index]

    def print_state(self):
        print(self.current_rule().name + ", " + self.current_seed().name())

    def offset_rule(self, offset):
        self.rule_index = (self.rule_index + offset) % len(self.rule_list)
        self.seed_index = 0
        self.print_state()
        return self.current_rule()

    def offset_seed(self, offset):
        self.seed_index = (self.seed_index + offset) % len(self.current_rule().seeds)
        self.print_state()
        return self.current_seed()

def moore_neighborhood():
     return [[1, 1, 1],
             [1, 0, 1],
             [1, 1, 1]]

def box_neighborhood(radius, center=True):
    neighborhood = np.ones((radius*2+1, radius*2+1))
    if not center:
        neighborhood[radius][radius] = 0
    return neighborhood

Rule = namedtuple("Rule", "name rule neighborhood seeds")

rules_list = RuleList([
    Rule(name = "amoeba",
         rule = [[1, 3, 5, 8], [3, 5, 7]],
         neighborhood = moore_neighborhood(),
         seeds = [RandomSeed(0.15)]),

    Rule(name = "anneal",
         rule = [[3, 5, 6, 7, 8], [4, 6, 7, 8]],
         neighborhood = moore_neighborhood(),
         seeds = [RandomSeed(0.50)]),

    Rule(name = "assimilation",
         rule = [[4, 5, 6, 7], [3, 4, 5]],
         neighborhood = moore_neighborhood(),
         seeds = [RandomSeed(0.17)]),

    Rule(name = "coagulations",
         rule = [[2, 3, 5, 6, 7, 8], [3, 7, 8]],
         neighborhood = moore_neighborhood(),
         seeds = [RandomSeed(0.06)]),

    Rule(name = "conway",
         rule = [[2, 3], [3]],
         neighborhood = moore_neighborhood(),
         seeds = [RandomSeed(0.5)]),

    Rule(name = "coral",
         rule = [[4, 5, 6, 7, 8], [3]],
         neighborhood = moore_neighborhood(),
         seeds = [RandomSeed(0.3)]),

    Rule(name = "day_and_night",
         rule = [[3, 4, 6, 7, 8], [3, 6, 7, 8]],
         neighborhood = moore_neighborhood(),
         seeds = [RandomSeed(0.5)]),

    Rule(name = "diamoeba",
         rule = [[5, 6, 7, 8], [3, 5, 6, 7, 8]],
         neighborhood = moore_neighborhood(),
         seeds = [RandomSeed(0.48)]),

    Rule(name = "flakes",
         rule = [[0, 1, 2, 3, 4, 5, 6, 7, 8], [3]],
         neighborhood = moore_neighborhood(),
         seeds = [SquareSeed(30)]),

    Rule(name = "gnarl",
         rule = [[1], [1]],
         neighborhood = moore_neighborhood(),
         seeds = [SquareSeed(1),
                  SquareSeed(2),
                  SquareSeed(4),
                  SquareSeed(5)]),

    Rule(name = "high_life",
         rule = [[2, 3], [3, 6]],
         neighborhood = moore_neighborhood(),
         seeds = [RandomSeed(0.5)]),

    Rule(name = "inverse_life",
         rule = [[3, 4, 6, 7, 8], [0, 1, 2, 3, 4, 7, 8]],
         neighborhood = moore_neighborhood(),
         seeds = [RandomSeed(0.5)]),

    Rule(name = "long_life",
         rule = [[5], [3, 4, 5]],
         neighborhood = moore_neighborhood(),
         seeds = [RandomSeed(0.2)]),

    Rule(name = "maze",
         rule = [[1, 2, 3, 4, 5], [3]],
         neighborhood = moore_neighborhood(),
         seeds = [RandomSeed(0.03),     
                  SquareSeed(7),
                  SquareSeed(8),
                  SquareSeed(9),
                  SquareSeed(10),
                  SquareSeed(64)]),

    Rule(name = "move",
         rule = [[2, 4, 5], [3, 6, 8]],
         neighborhood = moore_neighborhood(),
         seeds = [RandomSeed(0.5)]),

    Rule(name = "pseudo_life",
         rule = [[2, 3, 8], [3, 5, 7]],
         neighborhood = moore_neighborhood(),
         seeds = [RandomSeed(0.5)]),

    Rule(name = "replicator",
         rule = [[1, 3, 5, 7], [1, 3, 5, 7]],
         neighborhood = moore_neighborhood(),
         seeds = [SquareSeed(1)]),

    Rule(name = "seeds",
         rule = [[], [2,]],
         neighborhood = moore_neighborhood(),
         seeds = [SquareSeed(2)]),

    Rule(name = "serviettes",
         rule = [[], [2, 3, 4]],
         neighborhood = moore_neighborhood(),
         seeds = [SquareSeed(2)]),

    Rule(name = "stains",
         rule = [[2, 3, 5, 6, 7, 8], [3, 6, 7, 8]],
         neighborhood = moore_neighborhood(),
         seeds = [RandomSeed(0.05), SquareSeed(7)]),

    Rule(name = "two_by_two",
         rule = [[1, 2, 5], [3, 6]],
         neighborhood = moore_neighborhood(),
         seeds = [RandomSeed(0.5)]),

    Rule(name = "walled_cities",
         rule = [[2, 3, 4, 5], [4, 5, 6, 7, 8]],
         neighborhood = moore_neighborhood(),
         seeds = [RandomSeed(0.2),
                  SquareSeed(62)]),

    Rule(name = "bugs",
         rule = [[[34, 58]], [[34, 45]]],
         neighborhood = box_neighborhood(radius=5),
         seeds = [RandomSeed(0.5)]),

    Rule(name = "bugs_movie",
         rule = [[[123, 212]], [[123, 170]]],
         neighborhood = box_neighborhood(radius=10),
         seeds = [RandomSeed(0.5)]),

    Rule(name = "globe",
         rule = [[[163, 223]], [[74, 252]]],
         neighborhood = box_neighborhood(radius=8, center=False),
         seeds = [SquareSeed(35),
                  SquareSeed(40),
                  SquareSeed(45)]),

    Rule(name = "majority",
         rule = [[[41, 81]], [[41, 81]]],
         neighborhood = box_neighborhood(radius=4),
         seeds = [RandomSeed(0.5)]),

    Rule(name = "majorly",
         rule = [[[113, 225]], [[113, 225]]],
         neighborhood = box_neighborhood(radius=7),
         seeds = [RandomSeed(0.5)]),

    Rule(name = "waffle",
         rule = [[[100, 200]],[[75, 170]]],
         neighborhood = box_neighborhood(radius=7),
         seeds = [SquareSeed(18)]),

    Rule(name = "34_life",
         rule = [[1, 2, 5], [3, 6]],
         neighborhood = moore_neighborhood(),
         seeds = [RandomSeed(0.1)]),

    Rule(name = "ltl59999",
         rule = [[[9, 9]], [[9, 9]]],
         neighborhood = box_neighborhood(radius=5),
         seeds = [RandomSeed(0.05)]),

    Rule(name = "ltl534473460",
         rule = [[[34, 60]], [[34, 47]]],
         neighborhood = box_neighborhood(radius=5),
         seeds = [RandomSeed(0.5)]),

    Rule(name = "ltl534413458",
         rule = [[[34, 58]], [[34, 41]]],
         neighborhood = box_neighborhood(radius=5),
         seeds = [RandomSeed(0.5)]),
])