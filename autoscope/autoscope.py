from luma.core.interface.serial import spi
from luma.oled.device import sh1106
from PIL import Image
import numpy as np
import RPi.GPIO as GPIO

from autoscope.rules import rules
from autoscope.automata import Automata

class Autoscope:
    DIMENSIONS = [64, 128]
    KEY1 = 21

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.KEY1, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.device = sh1106(spi(device=0, port=0))

        self.automata = Automata(find_rule("conway"), self.DIMENSIONS)
        self.automata.populate_random(0.5)

    def run(self):
        while True:
            if not GPIO.input(self.KEY1):
                self.automata.populate_random(0.5)
            self._render()
            self.automata.step()

    def _render(self):
        image = Image.frombytes(mode='1', 
                                size=self.automata.board.shape[::-1], 
                                data=np.packbits(self.automata.board, axis=1))
        self.device.display(image)

def find_rule(name):
    for rule in rules:
        if rule.name == name:
            return rule