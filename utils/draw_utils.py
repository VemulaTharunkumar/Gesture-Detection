import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

def draw_landmarks_on_frame(frame, hand_landmarks):
    """
    Draws the hand landmarks and connections on the given frame.
    """
    mp_drawing.draw_landmarks(
        frame, 
        hand_landmarks, 
        mp_hands.HAND_CONNECTIONS
    )
    return frame
