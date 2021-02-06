import numpy as np
from collections import namedtuple

class RuleList():
    def __init__(self, rule_list):
        self.rule_list = rule_list
        self.seed_list = [0.01, 0.1, 0.5, 0.9, 0.99]
        self.rule_index = 0
        self.seed_index = 2

    def current_rule(self):
        return self.rule_list[self.rule_index]

    def current_seed(self):
        return self.seed_list[self.seed_index]

    def offset_rule(self, offset):
        self.rule_index = (self.rule_index + offset) % len(self.rule_list)
        return self.current_rule()

    def offset_seed(self, offset):
        self.seed_index = (self.seed_index + offset) % len(self.seed_list)
        return self.current_seed()

def _moore_neighborhood():
     return [[1, 1, 1],
             [1, 0, 1],
             [1, 1, 1]]

def _box_neighborhood(radius, center=True):
    neighborhood = np.ones((radius*2+1, radius*2+1))
    if not center:
        neighborhood[radius][radius] = 0
    return neighborhood

Rule = namedtuple("Rule", "name rule neighborhood")

rules = [
    Rule(name = "amoeba",
         rule = [[1, 3, 5, 8], [3, 5, 7]],
         neighborhood = _moore_neighborhood()),

    Rule(name = "anneal",
         rule = [[3, 5, 6, 7, 8], [4, 6, 7, 8]],
         neighborhood = _moore_neighborhood()),

    Rule(name = "assimilation",
         rule = [[4, 5, 6, 7], [3, 4, 5]],
         neighborhood = _moore_neighborhood()),

    Rule(name = "coagulations",
         rule = [[2, 3, 5, 6, 7, 8], [3, 7, 8]],
         neighborhood = _moore_neighborhood()),

    Rule(name = "conway",
         rule = [[2, 3], [3]],
         neighborhood = _moore_neighborhood()),

    Rule(name = "coral",
         rule = [[4, 5, 6, 7, 8], [3]],
         neighborhood = _moore_neighborhood()),

    Rule(name = "day_and_night",
         rule = [[3, 4, 6, 7, 8], [3, 6, 7, 8]],
         neighborhood = _moore_neighborhood()),

    Rule(name = "diamoeba",
         rule = [[5, 6, 7, 8], [3, 5, 6, 7, 8]],
         neighborhood = _moore_neighborhood()),

    Rule(name = "flakes",
         rule = [[0, 1, 2, 3, 4, 5, 6, 7, 8], [3]],
         neighborhood = _moore_neighborhood()),

    Rule(name = "gnarl",
         rule = [[1], [1]],
         neighborhood = _moore_neighborhood()),

    Rule(name = "high_life",
         rule = [[2, 3], [3, 6]],
         neighborhood = _moore_neighborhood()),

    Rule(name = "inverse_life",
         rule = [[3, 4, 6, 7, 8], [0, 1, 2, 3, 4, 7, 8]],
         neighborhood = _moore_neighborhood()),

    Rule(name = "life_34",
         rule = [[1, 2, 5], [3, 6]],
         neighborhood = _moore_neighborhood()),

    Rule(name = "long_life",
         rule = [[5], [3, 4, 5]],
         neighborhood = _moore_neighborhood()),

    Rule(name = "maze",
         rule = [[1, 2, 3, 4, 5], [3]],
         neighborhood = _moore_neighborhood()),

    Rule(name = "move",
         rule = [[2, 4, 5], [3, 6, 8]],
         neighborhood = _moore_neighborhood()),

    Rule(name = "pseudo_life",
         rule = [[2, 3, 8], [3, 5, 7]],
         neighborhood = _moore_neighborhood()),

    Rule(name = "replicator",
         rule = [[1, 3, 5, 7], [1, 3, 5, 7]],
         neighborhood = _moore_neighborhood()),

    Rule(name = "seeds",
         rule = [[], [2,]],
         neighborhood = _moore_neighborhood()),

    Rule(name = "serviettes",
         rule = [[], [2, 3, 4]],
         neighborhood = _moore_neighborhood()),

    Rule(name = "stains",
         rule = [[2, 3, 5, 6, 7, 8], [3, 6, 7, 8]],
         neighborhood = _moore_neighborhood()),

    Rule(name = "two_by_two",
         rule = [[1, 2, 5], [3, 6]],
         neighborhood = _moore_neighborhood()),

    Rule(name = "walled_cities",
         rule = [[2, 3, 4, 5], [4, 5, 6, 7, 8]],
         neighborhood = _moore_neighborhood()),

    Rule(name = "bugs",
         rule = [[[34, 58]], [[34, 45]]],
         neighborhood = _box_neighborhood(radius=5)),

    Rule(name = "bugs_movie",
         rule = [[[123, 212]], [[123, 170]]],
         neighborhood = _box_neighborhood(radius=10)),

    Rule(name = "globe",
         rule = [[[163, 223]], [[74, 252]]],
         neighborhood = _box_neighborhood(radius=8, center=False)),

    Rule(name = "majority",
         rule = [[[41, 81]], [[41, 81]]],
         neighborhood = _box_neighborhood(radius=4)),

    Rule(name = "majorly",
         rule = [[[113, 225]], [[113, 225]]],
         neighborhood = _box_neighborhood(radius=7)),

    Rule(name = "waffle",
         rule = [[[100, 200]],[[75, 170]]],
         neighborhood = _box_neighborhood(radius=7)),

    Rule(name = "ltl59999",
         rule = [[[9, 9]], [[9, 9]]],
         neighborhood = _box_neighborhood(radius=5)),
 
    Rule(name = "ltl534473460",
         rule = [[[34, 60]], [[34, 47]]],
         neighborhood = _box_neighborhood(radius=5)),

    Rule(name = "ltl534413458",
         rule = [[[34, 58]], [[34, 41]]],
         neighborhood = _box_neighborhood(radius=5)),
]

rules_list = RuleList(rules)