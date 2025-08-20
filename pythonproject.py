import tkinter as tk
import cv2
import mediapipe as mp
import pyautogui
import time
import threading
from PIL import Image, ImageTk
import random

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)

is_running = False
GESTURE_THRESHOLD = 0.1

# Function to detect gestures
def detect_gesture(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

    index_extended = index_tip.y < thumb_tip.y - GESTURE_THRESHOLD
    middle_extended = middle_tip.y < thumb_tip.y - GESTURE_THRESHOLD
    ring_extended = ring_tip.y < thumb_tip.y - GESTURE_THRESHOLD
    pinky_extended = pinky_tip.y < thumb_tip.y - GESTURE_THRESHOLD
    thumb_extended = thumb_tip.y < index_tip.y - GESTURE_THRESHOLD

    if thumb_extended and pinky_extended and not (index_extended or middle_extended or ring_extended):
        return "rewind_video"
    elif index_extended and not (middle_extended or ring_extended or pinky_extended) and not thumb_extended:
        return "play_pause"
    elif index_extended and middle_extended and ring_extended and pinky_extended and not thumb_extended:
        return "forward_video"
    elif thumb_extended and not (index_extended or middle_extended or ring_extended or pinky_extended):
        return "volume_down"
    elif index_extended and middle_extended and not (ring_extended or pinky_extended) and not thumb_extended:
        return "volume_up"
    return None

# Function for gesture control
def gesture_control():
    global is_running
    cap = cv2.VideoCapture(0)
    cooldown_time = 0.2
    last_gesture_time = time.time()
    last_play_pause_state = False

    while is_running:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image.")
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                gesture = detect_gesture(hand_landmarks)
                current_time = time.time()

                if gesture and (current_time - last_gesture_time >= cooldown_time):
                    if gesture == "volume_up":
                        pyautogui.press('up')
                        print("Volume Up")
                    elif gesture == "volume_down":
                        pyautogui.press('down')
                        print("Volume Down")
                    elif gesture == "forward_video":
                        pyautogui.hotkey('right')
                        print("Forwarding Video 10 Seconds")
                    elif gesture == "rewind_video":
                        pyautogui.hotkey('left')
                        print("Rewinding Video 5 Seconds")
                    elif gesture == "play_pause":
                        last_play_pause_state = not last_play_pause_state
                        pyautogui.press('playpause')
                        print("Playing Video" if last_play_pause_state else "Paused Video")

                    last_gesture_time = current_time

                mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        cv2.imshow("Hand Gesture Volume Control", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def start_detection():
    global is_running
    is_running = True
    threading.Thread(target=gesture_control, daemon=True).start()

def stop_detection():
    global is_running
    is_running = False

# Change button color function
def change_button_color(button):
    button.config(bg="#" + ''.join([random.choice('0123456789ABCDEF') for _ in range(6)]))

# Function to update the background image
def update_image(event):
    global photo_image
    image_resized = image.resize((event.width, event.height), Image.LANCZOS)
    photo_image = ImageTk.PhotoImage(image_resized)
    canvas.create_image(0, 0, anchor='nw', image=photo_image)

# Create main window
root = tk.Tk()
root.title("Gesture Control")
root.geometry("600x700")
root.configure(bg="#e6f7ff")

# Load the background image
image_path = r"C:\Users\NithishKumar\Desktop\pp.jpg"  # Update with your image path
try:
    image = Image.open(image_path)
except Exception as e:
    print(f"Error loading image: {e}")
    image = None

# Create a canvas for the background image
canvas = tk.Canvas(root)
canvas.pack(fill=tk.BOTH, expand=True)

# Set the background image on first load
if image:
    photo_image = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor='nw', image=photo_image)

# Bind the resize event to update the image
canvas.bind("<Configure>", update_image)

# Create the title label
title_label = tk.Label(root, text="Control your media with gestures!", bg="#e6f7ff", font=("Arial", 20, "bold"))
title_label.place(relx=0.5, rely=0.05, anchor='center')



# Create buttons
start_button = tk.Button( text="Start Gesture Control", command=lambda: [start_detection(), change_button_color(start_button)], bg="#4CAF50", fg="white", font=("Arial", 12))
start_button.pack(pady=10, padx=30, fill=tk.X)

stop_button = tk.Button( text="Stop Gesture Control", command=lambda: [stop_detection(), change_button_color(stop_button)], bg="#FFA500", fg="white", font=("Arial", 12))
stop_button.pack(pady=10, padx=30, fill=tk.X)

exit_button = tk.Button( text="Exit", command=root.quit, bg="#DC143C", fg="white", font=("Arial", 12))
exit_button.pack(pady=10, padx=30, fill=tk.X)

# Start the Tkinter main loop
root.mainloop()
