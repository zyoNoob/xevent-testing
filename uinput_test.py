#!.venv/bin/python

import uinput
import time
import os

def check_permissions():
    if os.geteuid() != 0:
        print("This script requires root privileges to run.")
        print("Please run with sudo or as root.")
        exit(1)

check_permissions()

try:
    with uinput.Device([uinput.REL_X, uinput.REL_Y,
                        uinput.BTN_LEFT, uinput.BTN_RIGHT]) as device:
        print("Moving mouse cursor...")
        for i in range(20):
            device.emit(uinput.REL_X, 5)
            device.emit(uinput.REL_Y, 5)
            time.sleep(0.01)  # Add delay between movements
except Exception as e:
    print(f"An error occurred: {e}")