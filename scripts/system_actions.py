import pyautogui
def move_mouse(x, y):
    try:
        pyautogui.moveTo(x, y, duration=0.5)
        return f"Mouse moved to ({x}, {y})"
    except Exception as e:
        return f"Error moving: {e}"
def click_mouse():
    try: pyautogui.click(); return "Clicked"
    except Exception as e: return f"Error clicking: {e}"
def type_text(text):
    try: pyautogui.write(text, interval=0.05); return f"Typed: {text}"
    except Exception as e: return f"Error typing: {e}"
def get_screen_info():
    try: s = pyautogui.size(); return f"Screen: {s.width}x{s.height}"
    except: return "Screen unavailable"
