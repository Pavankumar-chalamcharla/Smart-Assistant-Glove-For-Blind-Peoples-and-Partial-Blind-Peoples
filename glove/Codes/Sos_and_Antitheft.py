import serial
import time
import RPi.GPIO as GPIO

# === Config ===
REED_PIN = 17  # GPIO17 (pin 11)
SOS_PIN = 27   # GPIO27 (pin 13)
PHONE_NUMBER = "+917013682456"

# === Setup ===
GPIO.setmode(GPIO.BCM)
GPIO.setup(REED_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SOS_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

gsm = serial.Serial("/dev/ttyAMA0", baudrate=115200, timeout=1)

def send_at(command, delay=2):
    gsm.write((command + "\r").encode())
    time.sleep(delay)
    while gsm.inWaiting():
        print(gsm.readline().decode(errors='ignore'))

def make_call(number):
    print(f"Calling {number}")
    send_at(f"ATD{number};")
    time.sleep(15)  # Let it ring
    send_at("ATH")
    print("Call ended.")

def send_sms(number, message):
    send_at("AT+CMGF=1")  # Text mode
    time.sleep(1)
    gsm.write(f'AT+CMGS="{number}"\r'.encode())
    time.sleep(1)
    gsm.write((message + "\x1A").encode())  # CTRL+Z
    time.sleep(3)
    print("SMS sent.")

def get_gps_location():
    # TODO: Integrate with your GPS module
    return "0"  # Dummy location for now

def alert_owner(reason):
    location = get_gps_location()
    message = f"{reason}\nGPS: {location}"
    make_call(PHONE_NUMBER)
    send_sms(PHONE_NUMBER, message)

# === Main Loop ===
print("Monitoring glove...")

last_reed = GPIO.input(REED_PIN)
sos_triggered = False

try:
    while True:
        reed_state = GPIO.input(REED_PIN)
        sos_state = GPIO.input(SOS_PIN)

        if last_reed == GPIO.HIGH and reed_state == GPIO.LOW:
            print("Magnet removed — Thef
