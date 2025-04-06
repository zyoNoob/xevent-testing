import Xlib
import Xlib.display
import Xlib.X
import Xlib.protocol.event
import Xlib.XK

display = Xlib.display.Display()
root = display.screen().root

# Use the specific window ID instead of searching
window_id = 0x4000005
try:
    target_window = display.create_resource_object('window', window_id)
except Xlib.error.XError:
    print(f"Window with ID {window_id} not found")
    exit(1)

# Send a key press event (e.g., '4')
keycode = display.keysym_to_keycode(Xlib.XK.XK_8)
event = Xlib.protocol.event.KeyPress(
    time=Xlib.X.CurrentTime,
    root=root,
    window=target_window,
    same_screen=1,
    child=Xlib.X.NONE,
    root_x=0,
    root_y=0,
    event_x=0,
    event_y=0,
    state=0,
    detail=keycode
)
target_window.send_event(event, propagate=True)

# Send a mouse click event at (100, 100) relative to the window
event = Xlib.protocol.event.ButtonPress(
    time=Xlib.X.CurrentTime,
    root=root,
    window=target_window,
    same_screen=1,
    child=Xlib.X.NONE,
    root_x=0,
    root_y=0,
    event_x=100,
    event_y=100,
    state=0,
    detail=1  # Button 1 (left click)
)
target_window.send_event(event, propagate=True)

display.flush()