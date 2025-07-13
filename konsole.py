#!/usr/bin/env python3

from core import home
from klib import konsole_renderer
from klib import konsole_controller

import time

MATRIX_ROWS = 64
MATRIX_COLS = 64
SPLASH_SCREEN_DURATION_SECONDS = 2
SPLASH_SCREEN_FRAMERATE = 30

def main():
    renderer = konsole_renderer.Renderer(MATRIX_ROWS, MATRIX_COLS)

    # splash screen
    init_brightness_multiplier = renderer.brightness_multiplier

    # fade into init brightness multiplier
    for j in range(SPLASH_SCREEN_FRAMERATE * SPLASH_SCREEN_DURATION_SECONDS):
        renderer.brightness_multiplier = j / 100 * init_brightness_multiplier

        renderer.clear()
        for i in range(64):
            renderer.draw_rect(0, i, 64, i, (i + 5, i + 5, i + 5))

        renderer.draw_text(16, 28, "KONSOLE", (255, 255, 255))
        renderer.present()

        time.sleep(SPLASH_SCREEN_DURATION_SECONDS / 100)

    controller = konsole_controller.Controller()
    controller.wait_for_interface(renderer)
    controller.start()
    
    home.run_main_loop(controller, renderer)

if __name__ == "__main__":
    main()