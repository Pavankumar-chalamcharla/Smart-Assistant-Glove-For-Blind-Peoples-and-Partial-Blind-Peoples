import cv2
import numpy as np
import base64
import threading
import math
import pyttsx3
import matplotlib.pyplot as plt
from inference_sdk import InferenceHTTPClient

# Initialize Roboflow API Client
API_KEY = "Hfr4ZybHkk275doaxQNB"
MODEL_ID = "pothole-detection-system-rnoh4/1"

CLIENT = InferenceHTTPClient(
    api_url="https://outline.roboflow.com",
    api_key=API_KEY
)

# Initialize USB Camera
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # Set width
cap.set(4, 480)  # Set height

if not cap.isOpened():
    print("Error: Could not open USB camera.")
    exit()

# Initialize text-to-speech engine
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 150)  # Set speech speed

# Store detections globally
detections = []
detection_lock = threading.Lock()

# Function to estimate distance from camera to pothole using (x, y)
def estimate_distance(x, y):
    return math.sqrt(x*2 + y*2)  # Approximate Euclidean distance

# Function to determine pothole direction
def get_direction(x_center, frame_width):
    if x_center < frame_width / 3:
        return "left"
    elif x_center > 2 * frame_width / 3:
        return "right"
    else:
        return "center"

# Function to announce pothole alerts
def announce_pothole(detected_potholes):
    if detected_potholes:
        for pothole in detected_potholes:
            direction = pothole["direction"]
            distance = pothole["distance"]
            message = f"Pothole detected {round(distance, 1)} millimeters ahead to the {direction}."
            print("[AUDIO] ", message)
            tts_engine.say(message)
        tts_engine.runAndWait()

# Function to send frame to API asynchronously
def detect_potholes(frame):
    global detections
    try:
        input_w, input_h = 320, 240  # API input size
        frame_small = cv2.resize(frame, (input_w, input_h))

        # Encode frame as Base64
        _, img_encoded = cv2.imencode('.jpg', frame_small)
        img_base64 = base64.b64encode(img_encoded).decode('utf-8')

        # API call
        response = CLIENT.infer(img_base64, model_id=MODEL_ID)

        # Debug: Print API Response
        print("API Response:", response)

        detected_potholes = []
        new_detections = []

        if response and "predictions" in response and response["predictions"]:
            for det in response["predictions"]:
                if 'points' in det and isinstance(det['points'], list):
                    # Scale points back to original frame size
                    scaled_points = [[int(pt["x"] * (640 / input_w)), int(pt["y"] * (480 / input_h))] for pt in det["points"]]
                    points_array = np.array(scaled_points, np.int32).reshape((-1, 1, 2))

                    # Get average pothole position (center of detected area)
                    avg_x = sum(pt[0] for pt in scaled_points) / len(scaled_points)
                    avg_y = sum(pt[1] for pt in scaled_points) / len(scaled_points)

                    # Calculate pothole distance
                    distance = estimate_distance(avg_x, avg_y)

                    # Get pothole direction
                    direction = get_direction(avg_x, 640)

                    # Store pothole detection for voice alert
                    detected_potholes.append({"direction": direction, "distance": distance})

                    # Store detections for drawing
                    new_detections.append(points_array)

        # Update detections safely
        with detection_lock:
            detections = new_detections

        # Announce detected potholes
        announce_pothole(detected_potholes)

    except Exception as e:
        print(f"API Error: {e}")

# Counter to control API call frequency
frame_count = 0

# Set up Matplotlib for real-time display
plt.ion()
fig, ax = plt.subplots()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    # Draw pothole detections
    with detection_lock:
        for points in detections:
            cv2.polylines(frame, [points], isClosed=True, color=(0, 255, 0), thickness=2)

    # Convert frame to RGB for Matplotlib
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Display frame with Matplotlib
    ax.clear()
    ax.imshow(frame_rgb)
    ax.axis("off")
    plt.pause(0.01)

    # Send frame to API every 10 frames
    if frame_count % 10 == 0:
        threading.Thread(target=detect_potholes, args=(frame.copy(),), daemon=True).start()

    frame_count += 1

# Release resources
cap.release()
plt.close()
