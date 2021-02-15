# AutomataScope

AutomataScope is an interactive demonstration of life-like cellular automata on a Raspberry Pi. The device renders 2d binary totalistic cellular automata, such as Conway's Game of Life, on a bright high-contrast OLED screen. The Python program uses a fast 2D convolution algorithm to provide good performance on the Pi Zero's limited CPU, around 10 fps.

Conway's Game of Life is of course supported, but so are many others totalistic cellular automata rules, such as the amazingly lifelike [Bugs](https://www.emis.de/journals/DMTCS/pdfpapers/dmAA0113.pdf). Many of these were sourced from the [Cellular Automata rules lexicon](http://psoup.math.wisc.edu/mcell/ca_rules.html).

## Recommended Parts

- [Raspberry Pi Zero](https://www.raspberrypi.org/products/raspberry-pi-zero-w/) (with sd card and headers)
- [Waveshare 1.3 inch OLED Hat](https://www.waveshare.com/1.3inch-oled-hat.htm)
- [Zebra Zero GPIO Case from C4Labs](https://www.c4labs.com/product/zebra-zero-case-raspberry-pi-zero-zero-w-color-and-upgrade-options/)
