import cv2
import joblib
import numpy as np
import os
import time
from collections import deque, Counter
from ultralytics import YOLO
import threading
import winsound
import tkinter as tk
from tkinter import messagebox
from twilio.rest import Client
import torch
from database import save_alert_to_db

# ---------------------------
# --- Emotion Detection Setup
# ---------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "emotion_model.pkl")

# Load trained emotion model
model = joblib.load(MODEL_PATH)

# Load Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Keep last 15 predictions for stable emotion detection
preds = deque(maxlen=15)
current_emotion = None

# ---------------------------
# --- Weapon Detection Setup
# ---------------------------
YOLO_MODEL_PATH = "yolov8n.pt"
CONFIDENCE_THRESHOLD = 0.35
TARGET_KEYWORDS = ["knife", "gun", "scissors", "weapon"]

print("Loading YOLO model for weapon detection...")
yolo_model = YOLO(YOLO_MODEL_PATH)
class_names = yolo_model.names
print("YOLO model loaded successfully.")

# Auto-detect device (GPU if available)
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# ---------------------------
# --- Alert & Notification System
# ---------------------------
def play_alert_sound():
    """Play a short beep alert sound."""
    frequency = 1000  # Hz
    duration = 700    # milliseconds
    winsound.Beep(frequency, duration)


def show_alert_popup(message):
    """Show popup message using Tkinter in a separate thread."""
    def popup():
        root = tk.Tk()
        root.withdraw()
        messagebox.showwarning("⚠ ALERT!", message)
        root.destroy()

    threading.Thread(target=popup).start()


def send_sms_alert(message):
    """Send SMS alert using Twilio API."""
    account_sid = "your Twilio Account SID"   # <-- Replace with your Twilio Account SID
    auth_token = "your Twilio Auth Token"     # <-- Replace with your Twilio Auth Token
    client = Client(account_sid, auth_token)

    try:
        client.messages.create(
            body=message,
            from_="your Twilio phone number",   # <-- Replace with your Twilio phone number
            to="your phone number"       # <-- Replace with your phone number (with country code)
        )
        print("✅ SMS alert sent successfully!")
    except Exception as e:
        print("❌ Failed to send SMS:", e)


# ---------------------------
# --- Main Camera Function
# ---------------------------
def start_camera():
    global current_emotion

    cap = cv2.VideoCapture(0)
    prev_time = 0
    frame_count = 0

    while True:
        success, frame = cap.read()
        if not success:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # --- Emotion Detection ---
        for (x, y, w, h) in faces:
            roi = gray[y:y+h, x:x+w]
            roi_resized = cv2.resize(roi, (48, 48)).flatten().reshape(1, -1) / 255.0
            emotion = model.predict(roi_resized)[0]
            preds.append(emotion)

            stable_emotion, count = Counter(preds).most_common(1)[0]
            if count >= 7:
                current_emotion = stable_emotion

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            if current_emotion:
                cv2.putText(frame, current_emotion, (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # --- Weapon Detection (Optimized) ---
        frame_count += 1
        flagged = []

        # Run YOLO only every 5th frame for speed
        if frame_count % 5 == 0:
            small_frame = cv2.resize(frame, (640, 480))
            results = yolo_model.predict(source=small_frame, conf=CONFIDENCE_THRESHOLD, verbose=False, device=device)
            res = results[0]

            if res.boxes is not None and len(res.boxes) > 0:
                for box in res.boxes:
                    cls_id = int(box.cls[0].item())
                    conf = float(box.conf[0].item())
                    name = class_names.get(cls_id, str(cls_id)).lower()

                    is_weapon_like = any(k in name for k in TARGET_KEYWORDS)
                    x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())

                    color = (0, 255, 0)
                    if is_weapon_like:
                        color = (0, 0, 255)
                        flagged.append((name, conf))
                    label = f"{name}:{conf:.2f}"
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(frame, label, (x1, y1 - 8),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        # --- If Weapon Detected ---
        if flagged:
            cv2.putText(frame, "⚠ WEAPON DETECTED!", (10, 40),
                        cv2.FONT_HERSHEY_DUPLEX, 1.0, (0, 0, 255), 3)

            ts = time.strftime("%Y%m%d_%H%M%S")
            image_name = f"weapon_alert_{ts}.jpg"
            cv2.imwrite(image_name, frame)

            weapon_detected = ", ".join([f"{name} ({conf:.2f})" for name, conf in flagged])
            alert_message = f"🚨 ALERT: Weapon detected ({weapon_detected}) with emotion '{current_emotion}'. Screenshot saved: {image_name}"

            # --- Trigger Alerts ---
            play_alert_sound()
            show_alert_popup(alert_message)
            send_sms_alert(alert_message)
            save_alert_to_db(
    emotion=current_emotion,
    weapon=weapon_detected,
    message=alert_message,
    image_name=image_name
)

            # # --- Save alert message to file ---
            # with open("alert.txt", "a", encoding="utf-8") as f:
            #  f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {alert_message}\n\n")


        # --- FPS Display ---
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time) if prev_time else 0.0
        prev_time = curr_time
        cv2.putText(frame, f"FPS: {fps:.1f}", (10, frame.shape[0] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

        cv2.imshow("Women Safety - Emotion + Weapon Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


# ---------------------------
# --- Run the camera
# ---------------------------
if __name__ == "__main__":
    start_camera()
