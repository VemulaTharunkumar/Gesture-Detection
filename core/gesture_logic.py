import mediapipe as mp
from config.settings import GESTURE_THRESHOLD

mp_hands = mp.solutions.hands

def detect_gesture(hand_landmarks):
    """
    Analyzes hand landmarks to detect specific gestures.
    Returns: String representing the gesture name or None.
    """
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

    # Check finger states (extended vs folded)
    # Note: In screen coordinates, y increases downwards. 
    # So "extended" usually means tip.y < lower_joint.y. 
    # But he logic originally used thumb tip as reference relative to other fingers for simplicity.
    
    # Original logic preserved:
    index_extended = index_tip.y < thumb_tip.y - GESTURE_THRESHOLD
    middle_extended = middle_tip.y < thumb_tip.y - GESTURE_THRESHOLD
    ring_extended = ring_tip.y < thumb_tip.y - GESTURE_THRESHOLD
    pinky_extended = pinky_tip.y < thumb_tip.y - GESTURE_THRESHOLD
    thumb_extended = thumb_tip.y < index_tip.y - GESTURE_THRESHOLD

    if index_extended and not (middle_extended or ring_extended or pinky_extended) and not thumb_extended:
        return "play_pause"
    elif index_extended and middle_extended and ring_extended and pinky_extended and not thumb_extended:
        return "forward_video"
    elif thumb_extended and not (index_extended or middle_extended or ring_extended or pinky_extended):
        return "volume_down"
    elif index_extended and middle_extended and not (ring_extended or pinky_extended) and not thumb_extended:
        return "volume_up"
    elif middle_extended and ring_extended and pinky_extended and not (thumb_extended or index_extended):
        return "open_youtube"

    return None
