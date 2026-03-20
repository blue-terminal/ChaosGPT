from PIL import ImageGrab
import os
import datetime

def capture_screen():
    """Capture the screen and save it to a file"""
    try:
        # Create outputs directory if it doesn't exist
        if not os.path.exists("outputs"):
            os.makedirs("outputs")
            
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"outputs/screenshot_{timestamp}.png"
        
        screenshot = ImageGrab.grab()
        screenshot.save(filename)
        
        return f"Screenshot saved to {filename}"
    except Exception as e:
        return f"Error capturing screen: {str(e)}"
