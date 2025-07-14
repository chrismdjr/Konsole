#!/usr/bin/env python3

from klib import konsole_controller
from klib import konsole_renderer

from PIL import Image, ImageDraw

import time
import random

TARGET_FRAMERATE = 60
BRUSH_COLORS = [
    (255, 0, 0),
    (255, 150, 0),
    (255, 255, 0),
    (0, 255, 0),
    (0, 0, 255),
    (150, 0, 255),
    (255, 117, 234),
    (255, 255, 255),
    (0, 0, 0)
]
MIN_BRUSH_SIZE = 1
MAX_BRUSH_SIZE = 100
BRUSH_SIZE_VELOCITY_EPSILON = 1

renderer = konsole_renderer.Renderer()

controller = konsole_controller.Controller()
controller.wait_for_interface(renderer)
controller.start()

brush_position = [32, 32]
brush_sensitivity = 1
arrow_key_brush_sensitivity = brush_sensitivity * 0.5
brush_size_sensitivity = 0.25
brush_active = False
brush_color_index = 0
brush_size = 1

image = Image.new("RGB", (64, 64))
draw = ImageDraw.Draw(image)

controller_velocity = [0, 0]
arrow_key_controller_velocity = [0, 0]
brush_size_velocity = 0

delta_time = 0
while True:
    frame_start_time = time.time()

    # get input
    controller_events = controller.poll_events()

    for controller_event in controller_events:
        if controller_event.event_type == konsole_controller.ControllerEventType.L3_X_AT_REST:
            controller_velocity[1] = 0

        elif controller_event.event_type == konsole_controller.ControllerEventType.L3_Y_AT_REST:
            controller_velocity[0] = 0

        elif controller_event.event_type in (konsole_controller.ControllerEventType.L3_UP, konsole_controller.ControllerEventType.L3_DOWN):
            controller_velocity[1] = brush_sensitivity * controller_event.value * 0.000025

        elif controller_event.event_type in (konsole_controller.ControllerEventType.L3_LEFT, konsole_controller.ControllerEventType.L3_RIGHT):
            controller_velocity[0] = brush_sensitivity * controller_event.value * 0.000025

        # arrow keys

        elif controller_event.event_type == konsole_controller.ControllerEventType.UP_ARROW_PRESS:
            arrow_key_controller_velocity[1] -= arrow_key_brush_sensitivity

        elif controller_event.event_type == konsole_controller.ControllerEventType.DOWN_ARROW_PRESS:
            arrow_key_controller_velocity[1] += arrow_key_brush_sensitivity

        elif controller_event.event_type == konsole_controller.ControllerEventType.UP_OR_DOWN_ARROW_RELEASE:
            arrow_key_controller_velocity[1] = 0

        elif controller_event.event_type == konsole_controller.ControllerEventType.LEFT_ARROW_PRESS:
            arrow_key_controller_velocity[0] -= arrow_key_brush_sensitivity

        elif controller_event.event_type == konsole_controller.ControllerEventType.RIGHT_ARROW_PRESS:
            arrow_key_controller_velocity[0] += arrow_key_brush_sensitivity

        elif controller_event.event_type == konsole_controller.ControllerEventType.LEFT_OR_RIGHT_ARROW_RELEASE:
            arrow_key_controller_velocity[0] = 0

        elif controller_event.event_type == konsole_controller.ControllerEventType.CIRCLE_PRESS:
            brush_active = True

        elif controller_event.event_type == konsole_controller.ControllerEventType.CIRCLE_RELEASE:
            brush_active = False

        elif controller_event.event_type == konsole_controller.ControllerEventType.L1_PRESS:
            brush_color_index -= 1

            if brush_color_index < 0:
                brush_color_index = len(BRUSH_COLORS) - 1

        elif controller_event.event_type == konsole_controller.ControllerEventType.R1_PRESS:
            brush_color_index += 1

            if brush_color_index >= len(BRUSH_COLORS):
                brush_color_index = 0

        elif controller_event.event_type == konsole_controller.ControllerEventType.L2_PRESS:
            brush_size_velocity = -brush_size_sensitivity * (controller_event.value + 32767) * 0.0001

        elif controller_event.event_type == konsole_controller.ControllerEventType.R2_PRESS:
            brush_size_velocity = brush_size_sensitivity * (controller_event.value + 32767) * 0.0001

        elif controller_event.event_type == konsole_controller.ControllerEventType.SQUARE_PRESS:
            image = Image.new("RGB", (64, 64))
            draw = ImageDraw.Draw(image)

    brush_position[0] += controller_velocity[0] + arrow_key_controller_velocity[0]
    brush_position[1] += controller_velocity[1] + arrow_key_controller_velocity[1]
    brush_position[0] = min(max(brush_position[0], 0), 64)
    brush_position[1] = min(max(brush_position[1], 0), 64)
    if abs(brush_size_velocity) >= BRUSH_SIZE_VELOCITY_EPSILON:
        brush_size += brush_size_velocity

    brush_size = min(max(brush_size, MIN_BRUSH_SIZE), MAX_BRUSH_SIZE)

    # render
    renderer.clear()

    renderer.draw_image(0, 0, image)

    brush_outline_color = (0, 0, 0) if BRUSH_COLORS[brush_color_index] != (0, 0, 0) else (255, 255, 255)
    renderer.draw_ellipse(
        brush_position[0] - brush_size / 2 - 1,
        brush_position[1] - brush_size / 2 - 1,
        brush_size + 2,
        brush_size + 2
    , brush_outline_color)

    
    renderer.draw_ellipse(
        brush_position[0] - brush_size / 2,
        brush_position[1] - brush_size / 2,
        brush_size,
        brush_size
    , BRUSH_COLORS[brush_color_index])

    if brush_active:
        draw.ellipse((
            brush_position[0] - brush_size / 2,
            brush_position[1] - brush_size / 2,
            brush_position[0] + brush_size / 2,
            brush_position[1] + brush_size / 2
        ), BRUSH_COLORS[brush_color_index])

    renderer.present()

    # calculate delta time
    delta_time = time.time() - frame_start_time
    time_to_sleep = max(1 / TARGET_FRAMERATE - delta_time, 0)
    time.sleep(time_to_sleep)
    delta_time += time_to_sleep