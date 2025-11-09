# camera.py
import random

class Camera:
    """Handles camera effects like shake"""
    
    def __init__(self):
        self.shake_amount = 0
        self.shake_duration = 0
        self.offset_x = 0
        self.offset_y = 0
    
    def start_shake(self, intensity=5, duration=10):
        """Start screen shake effect"""
        self.shake_amount = intensity
        self.shake_duration = duration
    
    def update(self):
        """Update camera shake"""
        if self.shake_duration > 0:
            self.offset_x = random.randint(-self.shake_amount, self.shake_amount)
            self.offset_y = random.randint(-self.shake_amount, self.shake_amount)
            self.shake_duration -= 1
        else:
            self.offset_x = 0
            self.offset_y = 0
    
    def apply(self, rect):
        """Apply camera offset to a rect"""
        return rect.move(self.offset_x, self.offset_y)
    
    def get_offset(self):
        """Get current camera offset"""
        return (self.offset_x, self.offset_y)
