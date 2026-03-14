import pyautogui
import webbrowser
import threading

# Global state
youtube_opened = False

def perform_action(gesture):
    """
    Executes the action corresponding to the detected gesture.
    """
    global youtube_opened

    if gesture == "volume_up":
        pyautogui.press('up')

    elif gesture == "volume_down":
        pyautogui.press('down')

    elif gesture == "forward_video":
        pyautogui.hotkey('right')

    elif gesture == "play_pause":
        pyautogui.press('playpause')

    elif gesture == "open_youtube":
        # Open only once
        if not youtube_opened:
            youtube_opened = True
            threading.Thread(
                target=lambda: webbrowser.open("https://www.youtube.com"),
                daemon=True
            ).start()