import Xlib.display
import Xlib.X
import Xlib.XK
import Xlib.ext.xtest
import time
import json
import subprocess
from pathlib import Path
import sys
import re

def get_window_id():
    """Get window ID using xwininfo"""
    try:
        print("Please click on the window you want to track...")
        result = subprocess.run(['xwininfo'], capture_output=True, text=True)
        
        # Look for the window ID line using regex
        window_id_match = re.search(r'Window id: (0x[0-9a-fA-F]+)', result.stdout)
        if window_id_match:
            window_id = window_id_match.group(1)
            return int(window_id, 16)
        
        print("Could not find window ID. Please try again.")
        return None
    except Exception as e:
        print(f"Error getting window ID: {e}")
        return None

def get_window_info(window_id):
    """Get window information using xwininfo"""
    try:
        # Get window info using xwininfo
        result = subprocess.run(['xwininfo', '-id', str(window_id)],
                              capture_output=True, text=True)
        
        info = {}
        for line in result.stdout.split('\n'):
            if 'Absolute upper-left X:' in line:
                info['abs_x'] = int(line.split()[-1])
            elif 'Absolute upper-left Y:' in line:
                info['abs_y'] = int(line.split()[-1])
            elif 'Width:' in line:
                info['width'] = int(line.split()[-1])
            elif 'Height:' in line:
                info['height'] = int(line.split()[-1])
        
        if not info:
            print("Could not get window information from xwininfo")
            return None
        
        info['id'] = window_id
        return info
    except Exception as e:
        print(f"Error getting window info: {e}")
        return None

def save_coordinates(window_id, x, y):
    """Save coordinates to a JSON file"""
    file_path = Path(f"coordinates.json")
    print(f"Saving to: {file_path.absolute()}")
    
    # Get existing coordinates if file exists
    coords = {}
    try:
        if file_path.exists():
            with open(file_path, 'r') as f:
                coords = json.load(f)
    except Exception as e:
        print(f"Error reading file: {e}")
    
    # Add new coordinate
    coords[f"{x}_{y}"] = {
        'x': x,
        'y': y,
        'timestamp': time.time()
    }
    
    # Save to file
    try:
        with open(file_path, 'w') as f:
            json.dump(coords, f, indent=4)
        print(f"Coordinates saved to {file_path.absolute()}")
    except Exception as e:
        print(f"Error writing to file: {e}")

def main():
    print("Coordinate Finder Utility")
    print("------------------------")
    
    # Get window ID
    window_id = get_window_id()
    if not window_id:
        print("Could not get window ID. Please try again.")
        sys.exit(1)
    
    # Get window info
    window_info = get_window_info(window_id)
    if not window_info:
        print("Could not get window information")
        sys.exit(1)
    
    print("\nWindow Information:")
    print(f"ID: {window_info['id']}")
    print(f"Size: {window_info['width']}x{window_info['height']}")
    print(f"Position: {window_info['abs_x']}, {window_info['abs_y']}")
    print("\nTo find coordinates:")
    print("1. Move your mouse to the desired position")
    print("2. Press any key to record the coordinates")
    print("3. Press 'q' to quit")
    
    # Create display connection
    display = Xlib.display.Display()
    root = display.screen().root
    
    # Set up key press event mask
    root.change_attributes(event_mask=Xlib.X.KeyPressMask)
    
    try:
        while True:
            # Get current mouse position
            pointer = root.query_pointer()
            x = pointer.root_x - window_info['abs_x']
            y = pointer.root_y - window_info['abs_y']
            
            # Print coordinates
            print(f"\rCurrent position: ({x}, {y})", end='')
            
            # Check for key press
            if display.pending_events():
                event = display.next_event()
                if event.type == Xlib.X.KeyPress:
                    # Get key symbol
                    keycode = event.detail
                    keysym = display.keycode_to_keysym(keycode, 0)
                    
                    if keysym == Xlib.XK.XK_q:
                        print("\nQuitting...")
                        break
                    
                    # Save coordinates
                    save_coordinates(window_id, x, y)
                    
                    # Move mouse back to center
                    Xlib.ext.xtest.fake_input(
                        display,
                        Xlib.X.MotionNotify,
                        x=window_info['width'] // 2,
                        y=window_info['height'] // 2
                    )
                    display.sync()
            
            # Small delay to prevent CPU usage from being too high
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nQuitting...")
    finally:
        display.close()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)