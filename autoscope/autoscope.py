import numpy as np
import RPi.GPIO as GPIO
import time
from itertools import cycle
from luma.core.interface.serial import spi
from luma.oled.device import sh1106
from PIL import Image, ImageDraw, ImageFont
from gpiozero import Button

from rules import rules_list
from automata import Automata

class Autoscope:
    DIMENSIONS = [64, 128]
    FONT = ImageFont.truetype("fonts/Unibody 8.ttf", size=8)

    def __init__(self):
        self._initalize_buttons()
        self.automata = Automata(rules_list.current_rule(), self.DIMENSIONS)
        self.automata.populate_random(0.5)
        self.start_time = time.time()
        self.paused = False
        self.average_fps = 0
        self.last_measured_time = time.time()

    def run(self):
        self.press.when_pressed = self._toggle_paused

        while True:
            if self.up.is_pressed: self._next_rule() 
            if self.down.is_pressed: self._previous_rule() 
            if self.key1.is_pressed: self._repopulate()
            time_elapsed = time.time() - self.start_time
            do_draw_name = self.key2.is_pressed or time_elapsed < 3
            do_draw_fps = self.key2.is_pressed
            self._render(do_draw_name, do_draw_fps)
            if not self.paused:
                self.automata.step()
            self._calculate_fps()

    def _initalize_buttons(self):
        GPIO.setmode(GPIO.BCM)
        self.key1 = Button(21)
        self.key2 = Button(20)
        self.press = Button(13)
        self.up = Button(6)
        self.down = Button(19)
        self.device = sh1106(spi(device=0, port=0))

    def _render(self, do_draw_name, do_draw_fps):
        image = Image.frombytes(
            mode='1', 
            size=self.automata.board.shape[::-1], 
            data=np.packbits(self.automata.board, axis=1))
        if do_draw_name: self._draw_name(image)
        if do_draw_fps: self._draw_fps(image)
        image = image.rotate(180)
        self.device.display(image)

    def _draw_name(self, image):
        text = rules_list.current_rule().name
        text_size = self.FONT.getsize(text)
        draw = ImageDraw.Draw(image)
        draw.rectangle(((0, 0), text_size), fill="black")
        draw.text((0, 0), text, fill="white", font=self.FONT)

    def _draw_fps(self, image):
        text = "%.1f fps" % self.average_fps
        text_size = self.FONT.getsize(text)
        draw = ImageDraw.Draw(image)
        background_box = ((0, 52), (text_size[0], text_size[1] + 52))
        draw.rectangle(background_box, fill="black")
        draw.text((0, 52), text, fill="white", font=self.FONT)

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

    def _toggle_paused(self):
        self.paused = not self.paused

    def _calculate_fps(self):
        time_elapsed = time.time() - self.last_measured_time
        self.last_measured_time = time.time()
        self.average_fps = 0.8 *  self.average_fps + (1.0 - 0.8) * 1 / time_elapsed
