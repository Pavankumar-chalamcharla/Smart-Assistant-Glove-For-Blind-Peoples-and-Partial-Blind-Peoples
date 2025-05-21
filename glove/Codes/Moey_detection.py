import cv2
import base64
import threading
import numpy as np
import pyttsx3
import queue
from inference_sdk import InferenceHTTPClient

# Initialize Text-to-Speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech

# Queue for TTS to avoid threading error
speech_queue = queue.Queue()
last_spoken = ""

# Roboflow API setup
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="URcGm2tIhNFKCcgHKdVw"
)
MODEL_ID = "money-4wmm0/1"

# Initialize USB webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # Width
cap.set(4, 480)  # Height

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

detections = []
frame_count = 0

# Speak loop (runs in background thread)
def speech_loop():
    while True:
        text = speech_queue.get()
        if text:
            engine.say(f"Detected {text}")
            engine.runAndWait()

# Start the speech loop
threading.Thread(target=speech_loop, daemon=True).start()

# Add to speech queue only if not already spoken
def speak(text):
    global last_spoken
    if text != last_spoken:
        speech_queue.put(text)
        last_spoken = text

# Function to detect money
def detect_money(frame):
    global detections
    try:
        resized = cv2.resize(frame, (640, 480))
        _, buffer = cv2.imencode('.jpg', resized)
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        response = CLIENT.infer(img_base64, model_id=MODEL_ID)
        detections = response.get("predictions", [])
    except Exception as e:
        print(f"[ERROR] Roboflow API failed: {e}")

# Main loop
while True:
    ret, frame = cap.read()
    if not ret:
        break

    for pred in detections:
        x = int(pred['x'] - pred['width'] / 2)
        y = int(pred['y'] - pred['height'] / 2)
        w = int(pred['width'])
        h = int(pred['height'])

        class_name = pred['class']
        display_text = class_name.split('-')[1] if '-' in class_name else class_name

        speak(display_text)

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, display_text, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

    cv2.imshow("Roboflow Money Detection", frame)

    if frame_count % 10 == 0:
        threading.Thread(target=detect_money, args=(frame.copy(),), daemon=True).start()

    frame_count += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
