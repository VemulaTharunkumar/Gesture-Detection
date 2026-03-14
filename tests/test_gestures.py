import unittest
from core.gesture_logic import detect_gesture

class TestGestures(unittest.TestCase):
    def test_import(self):
        # Basic check to ensure module is importable
        self.assertTrue(callable(detect_gesture))

if __name__ == '__main__':
    unittest.main()
