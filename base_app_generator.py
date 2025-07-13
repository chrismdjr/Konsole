#!/usr/bin/env python3

import json
import os
import uuid

APPMETA_VERSION = 0
APPS_DIR_PATH = "apps/"
ENTRY_POINT_TEMPLATE_CODE = """#!/usr/bin/env python3

from klib import konsole_controller
from klib import konsole_renderer

MATRIX_ROWS = 64
MATRIX_COLS = 64

renderer = konsole_renderer.Renderer(MATRIX_ROWS, MATRIX_COLS)

controller = konsole_controller.Controller()
controller.wait_for_interface(renderer)
controller.start()"""

def main():
    print(f"AppMeta version: {APPMETA_VERSION}")
    app_id_prefix = input("ID prefix (optional): ")
    app_name = input("Name: ")
    entry_point_path = input("Entry point path: ")

    if app_id_prefix != "":
        mangled_app_id = f"{app_id_prefix}_{str(uuid.uuid4())}"

    else:
        mangled_app_id = str(uuid.uuid4())

    generated_appmeta_json = {
        "appmeta_version": APPMETA_VERSION,
        "id": mangled_app_id,
        "name": app_name,
        "entry_point_path": entry_point_path
    }

    print("Generating base app")

    app_dir_path = os.path.join(APPS_DIR_PATH, mangled_app_id)
    os.mkdir(app_dir_path)

    with open(f"{app_dir_path}/appmeta.json", "w") as f:
        f.write(json.dumps(generated_appmeta_json, indent=4))

    with open(f"{app_dir_path}/{entry_point_path}", "w") as f:
        f.write(ENTRY_POINT_TEMPLATE_CODE)

    os.symlink(
        os.path.abspath("klib"),
        os.path.abspath(f"{app_dir_path}/klib"),
        target_is_directory=True
    )

    print(f"Generated app {mangled_app_id}")

if __name__ == "__main__":
    main()