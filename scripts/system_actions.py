import pyautogui
import platform

def move_mouse(x, y):
    """Move the mouse to the specified coordinates"""
    try:
        pyautogui.moveTo(int(x), int(y), duration=0.25)
        return f"Mouse moved to ({x}, {y})"
    except Exception as e:
        return f"Error moving mouse: {str(e)}"

def click_mouse():
    """Click the mouse"""
    try:
        pyautogui.click()
        return "Mouse clicked"
    except Exception as e:
        return f"Error clicking mouse: {str(e)}"

def type_text(text):
    """Type the specified text"""
    try:
        pyautogui.write(text, interval=0.1)
        return f"Typed: {text}"
    except Exception as e:
        return f"Error typing text: {str(e)}"

def press_key(key):
    """Press a key"""
    try:
        pyautogui.press(key)
        return f"Key pressed: {key}"
    except Exception as e:
        return f"Error pressing key: {str(e)}"

def get_screen_info():
    """Get screen resolution and mouse position"""
    try:
        width, height = pyautogui.size()
        mouse_x, mouse_y = pyautogui.position()
        return f"Screen size: {width}x{height}, Mouse position: ({mouse_x}, {mouse_y})"
    except Exception as e:
        return f"Error getting screen info: {str(e)}"

def list_windows():
    """List all open windows with their coordinates (Linux version)"""
    try:
        import Xlib
        import Xlib.display
        
        display = Xlib.display.Display()
        root = display.screen().root
        window_ids = root.get_full_property(display.intern_atom('_NET_CLIENT_LIST'), Xlib.X.get_property_target).value
        
        window_list = []
        for window_id in window_ids:
            window = display.create_resource_object('window', window_id)
            name = window.get_wm_name()
            if name:
                geom = window.get_geometry()
                # Try to get absolute position
                try:
                    t_window = window
                    x, y = 0, 0
                    while t_window.id != root.id:
                        geom = t_window.get_geometry()
                        x += geom.x
                        y += geom.y
                        t_window = t_window.query_tree().parent
                    window_list.append(f"Title: '{name}', Box: (x={x}, y={y}, w={geom.width}, h={geom.height})")
                except:
                    window_list.append(f"Title: '{name}', Box: (x={geom.x}, y={geom.y}, w={geom.width}, h={geom.height})")
        
        return "\n".join(window_list) if window_list else "No titled windows found."
    except Exception as e:
        # Fallback to wmctrl if available
        import subprocess
        try:
            output = subprocess.check_output(["wmctrl", "-lG"]).decode()
            return output
        except:
            return f"Error listing windows: {str(e)}"

def drag_mouse(x, y):
    """Drag the mouse to the specified coordinates"""
    try:
        pyautogui.dragTo(int(x), int(y), duration=0.5)
        return f"Mouse dragged to ({x}, {y})"
    except Exception as e:
        return f"Error dragging mouse: {str(e)}"
