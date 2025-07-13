from klib import konsole_controller

import time
import os
import json
import subprocess

HOME_TARGET_FRAMERATE = 30
APPMETA_VERSION = 0
APPS_DIR_PATH = "apps/"

class App:
    def __init__(
        self,
        appmeta_version,
        app_id,
        name,
        entry_point_path
    ):
        self.appmeta_version = appmeta_version
        self.app_id = app_id
        self.name = name
        self.entry_point_path = entry_point_path

def _load_apps():
    loaded_apps = []

    for app_dir in os.listdir(APPS_DIR_PATH):
        app_appmeta_path = os.path.join(APPS_DIR_PATH, f"{app_dir}/appmeta.json")
        app_appmeta_json = json.loads(open(app_appmeta_path, "r").read())
        app_appmeta_version = app_appmeta_json["appmeta_version"]

        if app_appmeta_version != APPMETA_VERSION:
            print(f"Found app with incompatible AppMeta version (expected {APPMETA_VERSION}, found {app_appmeta_version}), skipping it")
            continue

        new_app = App(
            app_appmeta_version,
            app_appmeta_json["id"],
            app_appmeta_json["name"],
            app_appmeta_json["entry_point_path"]
        )
        loaded_apps.append(new_app)

    # alphabetize
    return sorted(loaded_apps, key=lambda app: app.name)

def run_main_loop(controller, renderer):
    selected_app_index = 0
    apps = _load_apps()
    app_process = None

    app_height_pixels = 5
    input_cooldown_frames = 3
    input_cooldown_frames_left = 0
    input_move_threshold = 20000

    delta_time = 0
    while True:
        frame_start_time = time.time()

        # poll app process
        if app_process != None:
            return_code = app_process.poll()
            if return_code != None:
                # handle closing of app
                if return_code != 0:
                    renderer.clear()
                    renderer.draw_text(1, 0, f"APP CRASHED\nEXIT CODE: {return_code}", (255, 0, 0))
                    renderer.present()
                    time.sleep(5)

                app_process = None

        # get input
        controller_events = controller.poll_events()

        input_cooldown_frames_left -= 1
        if input_cooldown_frames_left <= 0:
            for controller_event in controller_events:
                if app_process == None:
                    if (controller_event.event_type in (konsole_controller.ControllerEventType.L3_DOWN, konsole_controller.ControllerEventType.R3_DOWN) and controller_event.value > input_move_threshold) or controller_event.event_type == konsole_controller.ControllerEventType.DOWN_ARROW_PRESS:
                        selected_app_index += 1
                        input_cooldown_frames_left = input_cooldown_frames
                        break

                    elif (controller_event.event_type in (konsole_controller.ControllerEventType.L3_UP, konsole_controller.ControllerEventType.R3_UP) and controller_event.value < -input_move_threshold) or controller_event.event_type == konsole_controller.ControllerEventType.UP_ARROW_PRESS:
                        selected_app_index -= 1
                        input_cooldown_frames_left = input_cooldown_frames
                        break

                    elif controller_event.event_type == konsole_controller.ControllerEventType.CIRCLE_PRESS:
                        renderer.clear(clear_matrix=True)
                        app_process = subprocess.Popen(["python3", os.path.join(APPS_DIR_PATH, f"{apps[selected_app_index].app_id}/{apps[selected_app_index].entry_point_path}")])
                        break

                    elif controller_event.event_type == konsole_controller.ControllerEventType.TRIANGLE_PRESS:
                        apps = _load_apps()
                        renderer.clear()
                        renderer.draw_text(1, 0, f"RELOADED APPS", (255, 255, 255))
                        renderer.present()
                        time.sleep(0.5)
                        break

                else:
                    if controller_event.event_type == konsole_controller.ControllerEventType.PLAYSTATION_BUTTON_PRESS:
                        app_process.kill()
                        app_process = None
                        break

        selected_app_index = max(min(selected_app_index, len(apps) - 1), 0)

        # render
        if app_process != None:
            continue

        renderer.clear()

        # draw apps
        if len(apps) > 0:
            renderer.draw_rect(0, 32, 64, 5, (255, 255, 255))
            renderer.draw_text(1, 32, apps[selected_app_index].name, (0, 0, 0))

            for i, app in enumerate(apps):
                if i == selected_app_index:
                    continue

                renderer.draw_text(1, (i - selected_app_index) * app_height_pixels + 32, app.name, (100, 100, 100))

        else:
            renderer.draw_text(4, 32, "NO APPS LOADED", (255, 255, 255))

        # draw header
        for i in range(64):
            renderer.draw_rect(i, 0, i, 5, (64 - i + 5, 64 - i + 5, 64 - i + 5))

        renderer.draw_text(1, 0, "HOME", (255, 255, 255))

        renderer.present()

        # calculate delta time
        delta_time = time.time() - frame_start_time
        time_to_sleep = max(1 / HOME_TARGET_FRAMERATE - delta_time, 0)
        time.sleep(time_to_sleep)
        delta_time += time_to_sleep