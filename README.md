# Gesture Drawing AI 🎨🤖

Draw, erase, and switch colors using only your fingers — no stylus or touch required. This AI-powered virtual drawing app uses real-time finger gesture recognition powered by MediaPipe and OpenCV.

## 🚀 Features

- ✍️ **Finger Drawing:** Draw with your index finger in the air.
- 🎨 **Color Selection:** Touch index and middle fingers to select colors from the top palette.
- 🧽 **Eraser Mode:** Select the eraser the same way as colors.
- ⚡ **Real-Time Performance:** Lightweight and optimized for smooth, real-time tracking.
- 🤖 **Hand Tracking:** Powered by MediaPipe for accurate finger position detection.
- 🖼️ **Canvas Control:** Easy to use, fully dynamic canvas with no hardware accessories.

## 🛠️ Tech Stack

- **Python**
- **OpenCV** – for capturing video frames and drawing operations.
- **MediaPipe** – for real-time hand landmark detection and gesture tracking.
- **NumPy** – for image processing and frame manipulation.

## 🧠 How It Works

1. **Capture Feed:** OpenCV accesses the webcam stream.
2. **Hand Detection:** MediaPipe detects the hand and tracks landmarks.
3. **Gesture Logic:**
   - One finger (index) up → Drawing mode.
   - Two fingers (index + middle) touching → Color or eraser selection.
4. **Draw or Erase:** Based on selection, lines are drawn or erased on the canvas.
5. **Render:** The updated frame is shown with the current strokes.

## 🧩 Installation

```bash
git clone https://github.com/yourusername/gesture-drawing-ai.git
cd gesture-drawing-ai
pip install -r requirements.txt
python main.py
