import Xlib
import Xlib.display
import Xlib.X
import Xlib.protocol.event
import Xlib.XK
from Xlib.ext import xtest
import subprocess
import time

def get_window_info(window_id):
    """Get window information using xwininfo"""
    try:
        result = subprocess.run(['xwininfo', '-id', str(window_id)],
                              capture_output=True, text=True)
        
        info = {}
        for line in result.stdout.split('\n'):
            if 'Absolute upper-left X:' in line:
                info['x'] = int(line.split()[-1])
            elif 'Absolute upper-left Y:' in line:
                info['y'] = int(line.split()[-1])
            elif 'Width:' in line:
                info['width'] = int(line.split()[-1])
            elif 'Height:' in line:
                info['height'] = int(line.split()[-1])
        
        return info
    except Exception as e:
        print(f"Error getting window info: {e}")
        return None

display = Xlib.display.Display()
root = display.screen().root

# Use the specific window ID instead of searching
window_id = 0x4400005
try:
    target_window = display.create_resource_object('window', window_id)
except Xlib.error.XError:
    print(f"Window with ID {window_id} not found")
    exit(1)

# Get window information
window_info = get_window_info(window_id)
if window_info:
    print(f"Window info: {window_info}")
else:
    print("Could not get window info")
    exit(1)

# Make the window active by setting focus
event = Xlib.protocol.event.FocusIn(
    time=Xlib.X.CurrentTime,
    window=target_window,
    mode=Xlib.X.NotifyNormal,
    detail=Xlib.X.NotifyAncestor
)
target_window.send_event(event, propagate=True)
display.flush()
time.sleep(0.1)

relative_x = 2092
relative_y = 722

def click_position(x, y):
    relative_x = x
    relative_y = y

    # Pretend that mouse moved
    motion_event = Xlib.protocol.event.MotionNotify(
        time=Xlib.X.CurrentTime,
        root=display.screen().root,
        window=target_window,
        same_screen=1,
        child=Xlib.X.NONE,
        root_x=0,    # Root coordinates don't matter for root window
        root_y=0,    # Root coordinates don't matter for root window
        event_x=relative_x,     # Relative position within window
        event_y=relative_y,     # Relative position within window
        state=0,  # No modifier keys
        is_hint=0,
        detail=0
    )
    target_window.send_event(motion_event, propagate=True)
    display.flush()
    time.sleep(0.05)

    # Create mouse press event
    event = Xlib.protocol.event.ButtonPress(
        time=Xlib.X.CurrentTime,
        root=root,
        window=target_window,
        same_screen=1,
        child=Xlib.X.NONE,
        root_x=0,    # Root coordinates don't matter for root window
        root_y=0,    # Root coordinates don't matter for root window
        event_x=relative_x,     # Relative position within window
        event_y=relative_y,     # Relative position within window
        state=0,
        detail=1  # Button 1 (left click)
    )
    target_window.send_event(event, propagate=True)
    display.flush()
    time.sleep(0.05)

    # Create mouse release event
    event = Xlib.protocol.event.ButtonRelease(
        time=Xlib.X.CurrentTime,
        root=root, 
        window=target_window,
        same_screen=1,
        child=Xlib.X.NONE,
        root_x=0,     # Root coordinates don't matter for root window
        root_y=0,    # Root coordinates don't matter for root window
        event_x=relative_x,     # Relative position within window
        event_y=relative_y,     # Relative position within window
        state=0,
        detail=1  # Button 1 (left click)
    )
    target_window.send_event(event, propagate=True)
    display.flush()

click_position(relative_x, relative_y)