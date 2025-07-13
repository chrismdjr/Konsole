#!/usr/bin/env python3

from klib import konsole_controller
from klib import konsole_renderer

import time

MATRIX_ROWS = 64
MATRIX_COLS = 64

renderer = konsole_renderer.Renderer(MATRIX_ROWS, MATRIX_COLS)

controller = konsole_controller.Controller()
controller.wait_for_interface(renderer)
controller.start()

renderer.clear()
renderer.draw_text(0, 0, "TODO", (255, 255, 255))
renderer.present()

time.sleep(2)