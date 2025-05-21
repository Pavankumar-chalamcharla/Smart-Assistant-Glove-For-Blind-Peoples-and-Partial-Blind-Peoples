# Smart-Assistant-Glove-For-Blind-Peoples-and-Partial-Blind-Peoples
An AI-powered wearable glove designed to enhance safety, independence, and situational awareness for blind and partially blind individuals. Built using Raspberry Pi and smart sensors, this glove provides real-time feedback through vibration and audio, assisting users in navigating their surroundings safely and effectively.

---

## 🚀 Features

- 🎯 **Money Detection**  
  Detects Indian currency denominations using YOLOv8 and Roboflow API, triggering vibration feedback:
  - ₹10 = 1 vibration  
  - ₹20 = 2 vibrations  
  - ₹50 = 3 vibrations  
  - ₹100 = 4 vibrations  
  - ₹200 = 5 vibrations  
  - ₹500 = 6 vibrations

- 🕳️ **Pothole Detection**  
  Detects left or right potholes using IR sensor; triggers motor vibration:
  - 1 vibration = right-side pothole  
  - 2 vibrations = left-side pothole

- 🌡️ **Temperature Sensing**  
  Classifies objects as:
  - **Hot** (≥ 40°C)  
  - **Cold** (≤ 15°C)

- 🔒 **Anti-Theft Mechanism**  
  A magnet-based locking system triggers GPS location tracking and emergency alerts if the glove is tampered with.

- 📍 **GPS Location Tracking**  
  Sends real-time GPS coordinates via SMS using the SIM900A GSM module.

- 📞 **SOS Calling & SMS**  
  Pressing the SOS button or unauthorized magnet removal automatically:
  - Sends an SMS and calls the emergency number `+91 90101 92624`.

- 🧠 **Voice Feedback (Bluetooth)**  
  Real-time alerts and object detection feedback via Bluetooth headset using `pyttsx3`.

- 📷 **Image Capture**  
  Automatically captures an image every 5 minutes using a USB or ESP32-CAM camera.

---

## 🧰 Hardware Used

- Raspberry Pi 5 (8GB RAM)
- MLX90614 Temperature Sensor  
- IR Sensor (Pothole Detection)  
- NEO-6M GPS Module  
- SIM900A GSM Module  
- ESP32-CAM / USB Camera  
- 3.7V 5000mAh Li-ion Batteries (x2)  
- Vibration Motor  
- Magnet + Reed Switch  
- Bluetooth Speaker (Boat Rockerz 330)

---

## 🖥️ Software Stack

- Python 3.10
- Thonny IDE
- YOLOv8 (Roboflow Inference API)
- libcamera (for camera interface)
- pyttsx3 (for TTS feedback)
- serial, RPi.GPIO, smbus2, time, requests

---

## 📁 File Structure

