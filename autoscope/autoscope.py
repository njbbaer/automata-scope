import numpy as np
import RPi.GPIO as GPIO
from itertools import cycle
from luma.core.interface.serial import spi
from luma.oled.device import sh1106
from PIL import Image
from gpiozero import Button
from autoscope.rules import rules_list
from autoscope.automata import Automata

class Autoscope:
    DIMENSIONS = [64, 128]


    def __init__(self):
        self._initalize_buttons()
        
        self.automata = Automata(rules_list.current_rule(), self.DIMENSIONS)
        self.automata.populate_random(0.5)

    def run(self):
        while True:
            if self.up.is_pressed: self._next_rule() 
            if self.down.is_pressed: self._previous_rule() 
            if self.key1.is_pressed: self._repopulate()
            self._render()
            self.automata.step()

    def _initalize_buttons(self):
        GPIO.setmode(GPIO.BCM)
        self.key1 = Button(21)
        self.up = Button(6)
        self.down = Button(19)
        self.device = sh1106(spi(device=0, port=0))

    def _render(self):
        image = Image.frombytes(mode='1', 
                                size=self.automata.board.shape[::-1], 
                                data=np.packbits(self.automata.board, axis=1))
        self.device.display(image)

    def _next_rule(self):
        self.automata = Automata(rules_list.next_rule(), self.DIMENSIONS)
        self._repopulate()

    def _previous_rule(self):
        self.automata = Automata(rules_list.previous_rule(), self.DIMENSIONS)
        self._repopulate()

    def _repopulate(self):
        self.automata.populate_random(0.5)