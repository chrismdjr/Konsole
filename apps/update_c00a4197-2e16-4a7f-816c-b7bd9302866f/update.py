#!/usr/bin/env python3

from klib import konsole_renderer
from klib import konsole_utils

import time
import subprocess
import os
import sys

renderer = konsole_renderer.Renderer()

def handle_failure():
    renderer.clear()
    renderer.draw_text(1, 0, "FAILED TO CHECK\nFOR UPDATES", (255, 0, 0))
    renderer.present()
    time.sleep(2)
    sys.exit(0)

renderer.clear()
renderer.draw_text(1, 0, "CHECKING\nFOR UPDATES", (255, 255, 255))
renderer.present()

current_commit_process = subprocess.Popen(["git", "rev-parse", "HEAD"], stdout=subprocess.PIPE)
current_commit_hash, current_commit_stderr = current_commit_process.communicate()

if current_commit_process.returncode != 0:
    handle_failure()

dir_stat = os.stat(".")
pull_process = subprocess.Popen(["sudo", "-u", f"#{dir_stat.st_uid}", "git", "pull"], stdout=subprocess.PIPE)
_, pull_stderr = pull_process.communicate()

if pull_process.returncode != 0:
    handle_failure()

new_commit_process = subprocess.Popen(["git", "rev-parse", "HEAD"], stdout=subprocess.PIPE)
new_commit_hash, new_commit_stderr = new_commit_process.communicate()

if new_commit_process.returncode != 0:
    handle_failure()

if new_commit_hash != current_commit_hash:
    konsole_utils.restart()

else:
    renderer.clear()
    renderer.draw_text(1, 0, "ALREADY\nUP-TO-DATE", (255, 255, 255))
    renderer.present()
    time.sleep(2)