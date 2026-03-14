import cv2
import threading
import time
from collections import deque

from config import settings
from core.hand_tracker import HandTracker
from core.gesture_logic import detect_gesture
from core.controller import perform_action
from utils.draw_utils import draw_landmarks_on_frame

class GestureEngine:
    def __init__(self):
        self.tracker = HandTracker(
            max_hands=1, 
            detection_con=0.7, 
            track_con=0.5
        )
        self.is_running = False
        self.cap = None
        self.lock = threading.Lock()
        self.last_gesture_time = 0.0
        
        # Stabilization
        self.recent_gestures = deque(maxlen=settings.STABILIZATION_BUFFER_LEN)
        self.active_gestures = set()

    def start(self):
        with self.lock:
            if not self.is_running:
                self.is_running = True
                self._open_camera()

    def stop(self):
        with self.lock:
            self.is_running = False
            self._close_camera()

    def _open_camera(self):
        if self.cap is None or not self.cap.isOpened():
            self.cap = cv2.VideoCapture(settings.CAMERA_INDEX, cv2.CAP_DSHOW)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, settings.CAMERA_WIDTH)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, settings.CAMERA_HEIGHT)

    def _close_camera(self):
        if self.cap is not None:
            try:
                self.cap.release()
            except Exception:
                pass
            self.cap = None

    def process_frame(self, frame):
        # 1. Detect Hands
        results = self.tracker.find_hands(frame)
        
        current_frame_gestures = set()

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # 2. Draw Landmarks
                draw_landmarks_on_frame(frame, hand_landmarks)
                
                # 3. Detect Gesture
                gesture = detect_gesture(hand_landmarks)
                
                if gesture:
                    self.recent_gestures.append(gesture)
                    # Stabilization check
                    if self.recent_gestures.count(gesture) >= settings.STABILIZATION_THRESHOLD:
                        current_frame_gestures.add(gesture)
                        
                        now = time.time()
                        if gesture not in self.active_gestures and now - self.last_gesture_time >= settings.COOLDOWN_TIME:
                            # 4. Perform Action
                            perform_action(gesture)
                            self.last_gesture_time = now

        # Update active gestures
        self.active_gestures.clear()
        self.active_gestures.update(current_frame_gestures)

        # Status Overlay
        status_text = "RUNNING" if self.is_running else "STOPPED"
        color = (0, 255, 0) if self.is_running else (0, 0, 255)
        cv2.putText(frame, f"Gesture Control: {status_text}", (10, 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        
        return frame

    def generate_frames(self):
        while True:
            with self.lock:
                running = self.is_running
            
            if not running:
                time.sleep(0.05)
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + b'' + b'\r\n')
                continue

            with self.lock:
                # Ensure camera is open if running
                self._open_camera()
                ok, frame = self.cap.read() if self.cap is not None else (False, None)

            if not ok or frame is None:
                time.sleep(0.05)
                continue

            frame = self.process_frame(frame)
            ret, buf = cv2.imencode('.jpg', frame)
            if not ret:
                continue
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buf.tobytes() + b'\r\n')
