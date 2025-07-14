#!/usr/bin/env python3

from klib import konsole_controller
from klib import konsole_renderer

import time

TARGET_FRAMERATE = 30

renderer = konsole_renderer.Renderer()

controller = konsole_controller.Controller()
controller.wait_for_interface(renderer)
controller.start()

input_cooldown_frames = 3
input_cooldown_frames_left = 0
input_move_threshold = 20000

delta_time = 0
while True:
    frame_start_time = time.time()

    # get input
    controller_events = controller.poll_events()

    input_cooldown_frames_left -= 1
    if input_cooldown_frames_left <= 0:
        for controller_event in controller_events:
            if controller_event.event_type in (konsole_controller.ControllerEventType.L3_UP, konsole_controller.ControllerEventType.R3_UP) and controller_event.value < -input_move_threshold:
                print("up")
                input_cooldown_frames_left = input_cooldown_frames
                break

            elif controller_event.event_type in (konsole_controller.ControllerEventType.L3_DOWN, konsole_controller.ControllerEventType.R3_DOWN) and controller_event.value > input_move_threshold:
                print("down")
                input_cooldown_frames_left = input_cooldown_frames
                break

            elif controller_event.event_type in (konsole_controller.ControllerEventType.L3_LEFT, konsole_controller.ControllerEventType.R3_LEFT) and controller_event.value < -input_move_threshold:
                print("left")
                input_cooldown_frames_left = input_cooldown_frames
                break

            elif controller_event.event_type in (konsole_controller.ControllerEventType.L3_RIGHT, konsole_controller.ControllerEventType.R3_RIGHT) and controller_event.value > input_move_threshold:
                print("right")
                input_cooldown_frames_left = input_cooldown_frames
                break

            elif controller_event.event_type == konsole_controller.ControllerEventType.CIRCLE_PRESS:
                print("circle")
                break

    # render
    renderer.clear()

    renderer.draw_ellipse(0, 0, 64, 64, (0, 0, 255))

    renderer.present()

    # calculate delta time
    delta_time = time.time() - frame_start_time
    time_to_sleep = max(1 / TARGET_FRAMERATE - delta_time, 0)
    time.sleep(time_to_sleep)
    delta_time += time_to_sleep