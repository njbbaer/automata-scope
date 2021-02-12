import numpy as np

class Seed:
  pass

class RandomSeed(Seed):
    def __init__(self, density):
        self.density = density

    def populate(self, board):
        new_board = np.random.uniform(size=board.shape) < self.density
        return new_board.astype(np.int)

    def name(self):
        return f'random d={self.density}'

class SquareSeed(Seed):
    def __init__(self, side):
        self.shape = [side, side]

    def populate(self, board):
        new_board = np.zeros(shape=board.shape, dtype=int)
        square = np.ones(shape=self.shape, dtype=int)
        pos = [
            int(board.shape[0]/2 - square.shape[0]/2),
            int(board.shape[1]/2 - square.shape[1]/2)
        ]
        new_board[
            pos[0]:pos[0]+self.shape[0],
            pos[1]:pos[1]+self.shape[1]
        ] = square
        return new_board

    def name(self):
        return f'square s={self.shape[0]}'