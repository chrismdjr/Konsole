#!/usr/bin/env python3

from klib import konsole_controller
from klib import konsole_renderer

from PIL import Image, ImageDraw

import time
import random

TARGET_FRAMERATE = 60

renderer = konsole_renderer.Renderer()

controller = konsole_controller.Controller()
controller.wait_for_interface(renderer)
controller.start()

brush_position = [32, 32]
brush_sensitivity = 1
brush_active = False

image = Image.new("RGB", (64, 64))
draw = ImageDraw.Draw(image)

controller_velocity = [0, 0]

delta_time = 0
while True:
    frame_start_time = time.time()

    # get input
    controller_events = controller.poll_events()

    for controller_event in controller_events:
        if controller_event.event_type == konsole_controller.ControllerEventType.L3_X_AT_REST:
            controller_velocity[1] = 0

        if controller_event.event_type == konsole_controller.ControllerEventType.L3_Y_AT_REST:
            controller_velocity[0] = 0

        if controller_event.event_type in (konsole_controller.ControllerEventType.L3_UP, konsole_controller.ControllerEventType.L3_DOWN):
            controller_velocity[1] = brush_sensitivity * controller_event.value * 0.000025

        if controller_event.event_type in (konsole_controller.ControllerEventType.L3_LEFT, konsole_controller.ControllerEventType.L3_RIGHT):
            controller_velocity[0] = brush_sensitivity * controller_event.value * 0.000025

        if controller_event.event_type == konsole_controller.ControllerEventType.CIRCLE_PRESS:
            brush_active = True

        if controller_event.event_type == konsole_controller.ControllerEventType.CIRCLE_RELEASE:
            brush_active = False

    brush_position[0] += controller_velocity[0]
    brush_position[1] += controller_velocity[1]

    # render
    renderer.clear()

    renderer.draw_image(0, 0, image)

    renderer.draw_ellipse(
        brush_position[0] - 1,
        brush_position[1] - 1,
        2,
        2
    , (0, 0, 0))

    renderer.draw_ellipse(
        brush_position[0] - 0.5,
        brush_position[1] - 0.5,
        1,
        1
    , (255, 255, 255))

    if brush_active:
        draw.rectangle((
            brush_position[0] - 0.5,
            brush_position[1] - 0.5,
            brush_position[0] + 0.5,
            brush_position[1] + 0.5
        ), (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        ))

    renderer.present()

    # calculate delta time
    delta_time = time.time() - frame_start_time
    time_to_sleep = max(1 / TARGET_FRAMERATE - delta_time, 0)
    time.sleep(time_to_sleep)
    delta_time += time_to_sleep