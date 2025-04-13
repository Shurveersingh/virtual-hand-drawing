#utils.py
import cv2
import numpy as np

class DrawingUtils:
    def __init__(self):
        self.color = (0, 0, 0)  # Default color: black
        self.colors = [(0, 0, 0), (0, 0, 255), (0, 255, 0), (255, 0, 0), (255, 255, 255)]  # Black, Red, Green, Blue, White (Eraser)
        self.color_positions = [(50, 50), (150, 50), (250, 50), (350, 50), (450, 50)]  # Positions of color options
        self.eraser_image = cv2.imread('eraser.png')  # Load the eraser image
        if self.eraser_image is None:
            self.eraser_image = np.ones((60, 60, 3), dtype="uint8") * 255  # Create a white square if image not found
        else:
            self.eraser_image = cv2.resize(self.eraser_image, (60, 60))  # Resize the eraser image to fit the designated area

    def set_color(self, color):
        self.color = color

    def draw_circle(self, canvas, center, radius):
        cv2.circle(canvas, center, radius, self.color, -1)

    def draw_rectangle(self, canvas, start_point, end_point):
        cv2.rectangle(canvas, start_point, end_point, self.color, -1)

    def draw_line(self, canvas, start_point, end_point, thickness=5):
        cv2.line(canvas, start_point, end_point, self.color, thickness)

    def draw_color_options(self, canvas):
        for color, pos in zip(self.colors, self.color_positions):
            cv2.circle(canvas, pos, 30, color, -1)  # Increased size to 30
        # Draw the eraser image
        eraser_pos = self.color_positions[-1]
        canvas[eraser_pos[1]-30:eraser_pos[1]+30, eraser_pos[0]-30:eraser_pos[0]+30] = self.eraser_image

    def check_color_selection(self, index_finger_tip):
        for color, pos in zip(self.colors, self.color_positions):
            distance = np.linalg.norm(np.array(index_finger_tip) - np.array(pos))
            if distance < 30:  # Increased size to 30
                self.set_color(color)
                return True
        return False
