#!/usr/bin/env python3

from klib import konsole_controller
from klib import konsole_renderer

import time
import sys
import subprocess
import os
import sys

renderer = konsole_renderer.Renderer()

controller = konsole_controller.Controller()
controller.wait_for_interface(renderer)
controller.start()

renderer.clear()
renderer.draw_text(1, 0, "CHECKING FOR\nUPDATES", (255, 255, 255))
renderer.present()

current_commit_process = subprocess.Popen(["git", "rev-parse", "HEAD"], stdout=subprocess.PIPE)
current_commit_hash, current_commit_stderr = current_commit_process.communicate()

pull_process = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE)
_, pull_stderr = pull_process.communicate()

new_commit_process = subprocess.Popen(["git", "rev-parse", "HEAD"], stdout=subprocess.PIPE)
new_commit_hash, new_commit_stderr = new_commit_process.communicate()

if new_commit_hash != current_commit_hash:
    renderer.clear()
    renderer.draw_text(1, 0, "UPDATE FOUND,\nRESTARTING", (255, 255, 255))
    renderer.present()
    time.sleep(2)

    os.kill(int(open("konsole.pid").read()), 15)
    sys.exit(0)

else:
    renderer.clear()
    renderer.draw_text(1, 0, "UP-TO-DATE", (255, 255, 255))
    renderer.present()
    time.sleep(2)