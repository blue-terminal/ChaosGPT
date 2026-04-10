import pyautogui
import os
import time

def capture_screen():
    if not os.path.exists("outputs"):
        os.makedirs("outputs")
    filename = f"outputs/screenshot_{int(time.time())}.png"
    try:
        # Prova prima con pyautogui
        pyautogui.screenshot(filename)
        return f"Screenshot saved to {filename}"
    except:
        # Fallback su scrot se pyautogui fallisce (comune su Linux)
        try:
            os.system(f"scrot {filename}")
            return f"Screenshot saved via scrot to {filename}"
        except Exception as e:
            return f"Screenshot failed: {e}"