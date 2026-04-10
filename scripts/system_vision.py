import pyautogui, os, time
def capture_screen():
    if not os.path.exists("outputs"): os.makedirs("outputs")
    fn = f"outputs/screen_{int(time.time())}.png"
    try: pyautogui.screenshot(fn); return f"Saved {fn}"
    except: 
        try: os.system(f"scrot {fn}"); return f"Saved via scrot {fn}"
        except Exception as e: return f"Screen failed: {e}"
