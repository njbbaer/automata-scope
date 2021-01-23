import time
import numpy as np
from luma.core.render import canvas

class Automata:
    def __init__(self, rule, shape):
        self.board = np.zeros(shape, dtype=int)
        self._set_rule(rule)

    def populate_random(self, density=0):
        self.board = np.random.uniform(size=self.board.shape) < density
        self.board = self.board.astype(np.int)

    def benchmark(self, iterations):
        start = time.process_time()
        for _ in range(iterations):
            self.step()
        delta = time.process_time() - start
        rate = iterations / delta
        print(iterations, "iterations of", self.board.shape, "cells in",
              "%.2f"%delta, "seconds at", "%.2f"%rate, "frames per second")

    def _set_rule(self, rule):
        self.neighborhood = rule.neighborhood
        get_ints = lambda x: [i for i in x if isinstance(i, int)]
        self.rule_ints = (get_ints(rule.rule[0]), get_ints(rule.rule[1]))
        get_ranges = lambda x: [i for i in x if not isinstance(i, int)]
        self.rule_ranges = (get_ranges(rule.rule[0]), get_ranges(rule.rule[1]))
        self._calculate_kernal_ft()

    def _calculate_kernal_ft(self):
        neighborhood = np.array(self.neighborhood)
        kernal = np.zeros(self.board.shape)
        n_height, n_width = neighborhood.shape
        b_height, b_width = self.board.shape
        kernal[(b_height - n_height - 1) // 2 : (b_height + n_height) // 2,
               (b_width - n_width - 1) // 2 : (b_width + n_width) // 2] = self.neighborhood
        self.kernal_ft = np.fft.fft2(kernal)

    def step(self):
        convolution = self._convolve2d()
        shape = convolution.shape
        new_board = np.zeros(shape)
        new_board[np.where(np.in1d(convolution, self.rule_ints[0]).reshape(shape)
                            & (self.board == 1))] = 1
        new_board[np.where(np.in1d(convolution, self.rule_ints[1]).reshape(shape)
                            & (self.board == 0))] = 1
        for rule_range in self.rule_ranges[0]:
            new_board[np.where((self.board == 1)
                                & (convolution >= rule_range[0]) 
                                & (convolution <= rule_range[1]))] = 1
        for rule_range in self.rule_ranges[1]:
            new_board[np.where((self.board == 0)
                                & (convolution >= rule_range[0]) 
                                & (convolution <= rule_range[1]))] = 1
        self.board = new_board.astype(int)
            
    def _convolve2d(self):
        board_ft = np.fft.fft2(self.board)
        convolution = np.fft.ifft2(board_ft * self.kernal_ft)
        height, width = board_ft.shape
        convolution = np.roll(convolution, - int(height / 2) + 1, axis=0)
        convolution = np.roll(convolution, - int(width / 2) + 1, axis=1)
        return convolution.round()