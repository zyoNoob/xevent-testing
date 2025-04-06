# X11 Event Testing

This project demonstrates how to send keyboard and mouse events to X11 windows using Python and the Xlib library.

## Features

- Send keyboard events to specific windows
- Send mouse click events at specific coordinates
- Target windows by ID for precise control

## Requirements

- Python 3.x
- Python Xlib package (`python-xlib`)

## Usage

1. First, identify the target window ID using `xwininfo`:
   ```bash
   xwininfo
   ```
   Click on the desired window to get its ID.

2. Update the `window_id` variable in `xlib_test.py` with your window's ID.

3. Run the script:
   ```bash
   python xlib_test.py
   ```

## Example

The current script is configured to:
- Send a key press event (key '8')
- Send a mouse click event at position (100,100) relative to the window

## Customization

To modify the behavior:
1. Change the window ID by updating the `window_id` variable
2. Modify the key press by changing `Xlib.XK.XK_8` to another key
3. Adjust the mouse click position by changing `event_x` and `event_y` coordinates

## Notes

- The script requires appropriate permissions to send events to windows
- Some applications may block or ignore synthetic events for security reasons
- The window must be active and visible for events to be properly received