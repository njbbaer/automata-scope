import numpy as np
import RPi.GPIO as GPIO
import time
from itertools import cycle
from luma.core.interface.serial import spi
from luma.oled.device import sh1106
from PIL import Image, ImageDraw, ImageFont
from gpiozero import Button
from autoscope.rules import rules_list
from autoscope.automata import Automata

class Autoscope:
    DIMENSIONS = [64, 128]

    def __init__(self):
        self._initalize_buttons()
        self.automata = Automata(rules_list.current_rule(), self.DIMENSIONS)
        self.automata.populate_random(0.5)
        self.start_time = time.time()

    def run(self):
        while True:
            if self.up.is_pressed: self._next_rule() 
            if self.down.is_pressed: self._previous_rule() 
            if self.key1.is_pressed: self._repopulate()
            time_elapsed = time.time() - self.start_time
            draw_name = self.key2.is_pressed or time_elapsed < 3
            self._render(draw_name)
            self.automata.step()

    def _initalize_buttons(self):
        GPIO.setmode(GPIO.BCM)
        self.key1 = Button(21)
        self.key2 = Button(20)
        self.up = Button(6)
        self.down = Button(19)
        self.device = sh1106(spi(device=0, port=0))

    def _render(self, draw_name):
        image = Image.frombytes(mode='1', 
                                size=self.automata.board.shape[::-1], 
                                data=np.packbits(self.automata.board, axis=1))
        if draw_name: self._draw_name(image)
        image = image.rotate(180)
        self.device.display(image)

    def _draw_name(self, image):
        text = rules_list.current_rule().name
        font = ImageFont.truetype("fonts/Unibody 8.ttf", size=8)
        text_size = font.getsize(text)
        draw = ImageDraw.Draw(image)
        draw.rectangle(((0, 0), text_size), fill="black")
        draw.text((0, 0), text, fill="white", font=font)

    def _next_rule(self):
        self.automata = Automata(rules_list.next_rule(), self.DIMENSIONS)
        self._repopulate()
        self.start_time = time.time()

    def _previous_rule(self):
        self.automata = Automata(rules_list.previous_rule(), self.DIMENSIONS)
        self._repopulate()
        self.start_time = time.time()

    def _repopulate(self):
        self.automata.populate_random(0.5)