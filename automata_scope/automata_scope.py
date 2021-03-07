import numpy as np
import time
from itertools import cycle
from luma.core.interface.serial import spi
from luma.oled.device import sh1106
from PIL import Image, ImageDraw, ImageFont
from gpiozero import Button

from rules_list import rules_list
from automata import Automata

class AutomataScope:
    DIMENSIONS = [64, 128]
    FONT = ImageFont.truetype("/home/pi/automata-scope/fonts/Unibody 8.ttf", size=8)

    def __init__(self):
        self._initialize_buttons()
        self._initialize_button_events()
        self.device = sh1106(spi(device=0, port=0), rotate=2)
        self.device.contrast(255)
        self.automata = Automata(rules_list.current_rule(), self.DIMENSIONS)
        self._repopulate()
        self.start_time = time.time()
        self.paused = False
        self.average_fps = 0
        self.last_measured_time = time.time()

    def _initialize_buttons(self):
        self.key1 = Button(21)
        self.key2 = Button(20)
        self.key3 = Button(16)
        self.center = Button(13)
        self.up = Button(6)
        self.down = Button(19)
        self.left = Button(5)
        self.right = Button(26)

    def _initialize_button_events(self):
        self.down.when_pressed = self._next_rule
        self.up.when_pressed = self._previous_rule
        self.left.when_pressed = self._previous_seed
        self.right.when_pressed = self._right_button_pressed

    def run(self):
        while True:
            if self.center.is_pressed: self._repopulate()

            self._render()
            if not self._is_paused():
                self.automata.step()
            self._calculate_fps()

    def _render(self):
        image = Image.frombytes(
            mode='1', 
            size=self.automata.board.shape[::-1], 
            data=np.packbits(self.automata.board, axis=1))
        if self.key1.is_pressed: image = zoom_image(image)
        if self._do_draw_fps(): self._draw_fps(image)
        if self._do_draw_name():
            self._draw_name(image)
            self._draw_seed_name(image)
        self.device.display(image)

    def _do_draw_name(self):
        time_elapsed = time.time() - self.start_time
        return self.key3.is_pressed or time_elapsed < 3

    def _do_draw_fps(self):
        return self.key3.is_pressed

    def _is_paused(self):
        return self.key2.is_pressed

    def _draw_name(self, image):
        text = rules_list.current_rule().name
        text_size = self.FONT.getsize(text)
        draw = ImageDraw.Draw(image)
        draw.rectangle(((0, 0), text_size), fill="black")
        draw.text((0, 0), text, fill="white", font=self.FONT)

    def _draw_seed_name(self, image):
        text = rules_list.current_seed().name()
        text_size = self.FONT.getsize(text)
        draw = ImageDraw.Draw(image)
        background_box = ((0, 53), (text_size[0], text_size[1] + 53))
        draw.rectangle(background_box, fill="black")
        draw.text((0, 53), text, fill="white", font=self.FONT)

    def _draw_fps(self, image):
        text = "%.1f" % self.average_fps
        text_size = self.FONT.getsize(text)
        draw = ImageDraw.Draw(image)
        background_box = ((128, 0), (128 - text_size[0], text_size[1]))
        draw.rectangle(background_box, fill="black")
        draw.text((128 - text_size[0], 0), text, fill="white", font=self.FONT)

    def _next_rule(self, previous=False):
        offset = -1 if previous else 1
        self.automata = Automata(rules_list.offset_rule(offset), self.DIMENSIONS)
        self._repopulate()
        self.start_time = time.time()

    def _previous_rule(self):
        self._next_rule(previous=True)

    def _next_seed(self, previous=False):
        offset = -1 if previous else 1
        rules_list.offset_seed(offset)
        self._repopulate()
        self.start_time = time.time()

    def _previous_seed(self):
        self._next_seed(previous=True)

    def _repopulate(self):
        self.automata = Automata(rules_list.current_rule(), self.DIMENSIONS)
        self.automata.populate(rules_list.current_seed())

    def _calculate_fps(self):
        time_elapsed = time.time() - self.last_measured_time
        self.last_measured_time = time.time()
        self.average_fps = 0.8 * self.average_fps + (1.0 - 0.8) * 1 / time_elapsed

    def _right_button_pressed(self):
        if self.key2.is_pressed:
            self.automata.step()
        else:
            self._next_seed()

def zoom_image(image):
    w, h = image.size
    x, y = image.size[0] / 2, image.size[1] / 2
    image = image.crop((x - w / 4, y - h / 4, 
                    x + w / 4, y + h / 4))
    return image.resize((w, h), Image.LANCZOS)