import os
import time
import sys

def restart(renderer):
    # close main process
    os.kill(int(open("konsole.pid").read()), 15)

    # close app process if we're calling from an app
    sys.exit(0)