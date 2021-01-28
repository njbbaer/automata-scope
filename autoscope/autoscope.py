import numpy as np
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
        self._initialize_buttons()
        self._initialize_button_events()
        self.device = sh1106(spi(device=0, port=0), rotate=2)
        self.automata = Automata(rules_list.current_rule(), self.DIMENSIONS)
        self.automata.populate_random(0.5)
        self.start_time = time.time()
        self.paused = False
        self.average_fps = 0
        self.last_measured_time = time.time()

    def _initialize_buttons(self):
        self.key1 = Button(21)
        self.key2 = Button(20)
        self.press = Button(13)
        self.up = Button(6)
        self.down = Button(19)
        self.left = Button(5)
        self.right = Button(26)

    def _initialize_button_events(self):
        self.up.when_pressed = self._next_rule
        self.down.when_pressed = self._previous_rule
        self.right.when_pressed = self._right_button_pressed

    def run(self):
        while True:
            if self.press.is_pressed: self._repopulate()
            self.paused = self.key1.is_pressed
            do_draw_fps = self.key2.is_pressed

            self._render(self._do_draw_name(), do_draw_fps)
            if not self.paused:
                self.automata.step()
            self._calculate_fps()

    def _render(self, do_draw_name, do_draw_fps):
        image = Image.frombytes(
            mode='1', 
            size=self.automata.board.shape[::-1], 
            data=np.packbits(self.automata.board, axis=1))
        if do_draw_name: self._draw_name(image)
        if do_draw_fps: self._draw_fps(image)
        self.device.display(image)

    def _do_draw_name(self):
        time_elapsed = time.time() - self.start_time
        return self.key2.is_pressed or time_elapsed < 3

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

    def _calculate_fps(self):
        time_elapsed = time.time() - self.last_measured_time
        self.last_measured_time = time.time()
        self.average_fps = 0.8 *  self.average_fps + (1.0 - 0.8) * 1 / time_elapsed

    def _right_button_pressed(self):
        if self.key1.is_pressed: self.automata.step()