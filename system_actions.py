import pyautogui
import sys

def move_mouse(x, y):
    try:
        pyautogui.moveTo(x, y, duration=0.5)
        return f"Mouse moved to ({x}, {y})"
    except Exception as e:
        return f"Error moving mouse: {e}"

def click_mouse():
    try:
        pyautogui.click()
        return "Clicked mouse"
    except Exception as e:
        return f"Error clicking: {e}"

def type_text(text):
    try:
        pyautogui.write(text, interval=0.05)
        return f"Typed: {text}"
    except Exception as e:
        return f"Error typing: {e}"

def get_screen_info():
    try:
        size = pyautogui.size()
        return f"Screen: {size.width}x{size.height}"
    except:
        return "Screen info unavailable"

def close_tab():
    """Simula la chiusura di una scheda del browser tramite hotkey."""
    try:
        if sys.platform == "darwin":
            pyautogui.hotkey('command', 'w')
        else:
            pyautogui.hotkey('ctrl', 'w')
        return "Closed browser tab"
    except Exception as e:
        return f"Error closing tab: {e}"