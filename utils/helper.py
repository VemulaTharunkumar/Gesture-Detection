# Helper functions
# Currently empty as the main logic is simple threshold comparison.
# Future expansion: geometry, angle calculations, etc.

def calculate_distance(p1, p2):
    """
    Calculate Euclidean distance between two points (normalized or pixel).
    """
    return ((p1.x - p2.x)**2 + (p1.y - p2.y)**2)**0.5
