##first.py
import cv2
import mediapipe as mp
import numpy as np
from utils import DrawingUtils

# Initialize Mediapipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Initialize the drawing canvas
canvas = np.ones((720, 1280, 3), dtype="uint8") * 255  # Initialize as white

# Initialize the video capture
cap = cv2.VideoCapture(0)

# Initialize the previous position of the index finger tip
prev_index_finger_tip = None

# Initialize DrawingUtils
drawing_utils = DrawingUtils()

# Function to check if the index and middle fingers are close
def are_fingers_close(hand_landmarks, h, w):
    try:
        index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
        middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        index_finger_tip = (int(index_finger_tip.x * w), int(index_finger_tip.y * h))
        middle_finger_tip = (int(middle_finger_tip.x * w), int(middle_finger_tip.y * h))
        distance = np.linalg.norm(np.array(index_finger_tip) - np.array(middle_finger_tip))
        return distance < 40  # Adjust threshold as needed
    except Exception as e:
        print(f"Error in are_fingers_close: {e}")
        return False

while cap.isOpened():
    try:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break

        # Flip the frame horizontally for a later selfie-view display
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame and detect hands
        result = hands.process(frame_rgb)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Get the coordinates of the index finger tip
                index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

                # Convert normalized coordinates to pixel coordinates
                h, w, _ = frame.shape
                index_finger_tip = (int(index_finger_tip.x * w), int(index_finger_tip.y * h))

                # Draw the cursor at the index finger tip position
                cv2.circle(frame, index_finger_tip, 10, (0, 255, 255), -1)  # Yellow cursor

                # Check if the index and middle fingers are close for color selection
                if are_fingers_close(hand_landmarks, h, w):
                    if drawing_utils.check_color_selection(index_finger_tip):
                        prev_index_finger_tip = None  # Reset drawing if color is selected
                    continue

                # Draw with the index finger only if it is far from the middle finger
                if not are_fingers_close(hand_landmarks, h, w):
                    if prev_index_finger_tip is not None:
                        if drawing_utils.color == (255, 255, 255):  # Eraser
                            drawing_utils.draw_line(canvas, prev_index_finger_tip, index_finger_tip, thickness=30)  # Double the thickness
                        else:
                            drawing_utils.draw_line(canvas, prev_index_finger_tip, index_finger_tip)
                    prev_index_finger_tip = index_finger_tip
                else:
                    prev_index_finger_tip = None

        else:
            prev_index_finger_tip = None

        # Display the color options on the frame
        drawing_utils.draw_color_options(frame)

        # Ensure the canvas and frame have the same dimensions
        if canvas.shape[:2] != frame.shape[:2]:
            canvas = cv2.resize(canvas, (frame.shape[1], frame.shape[0]))

        # Overlay the canvas on the frame with adjusted blending weights
        frame = cv2.addWeighted(frame, 0.7, canvas, 0.3, 0)

        # Display the canvas and the frame
        cv2.imshow("Canvas", canvas)
        cv2.imshow("Frame", frame)

        if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
            break

    except Exception as e:
        print(f"Error in main loop: {e}")
        break

# Save the canvas to a file
try:
    cv2.imwrite("canvas_output.png", canvas)
except Exception as e:
    print(f"Error saving canvas: {e}")

cap.release()
cv2.destroyAllWindows()