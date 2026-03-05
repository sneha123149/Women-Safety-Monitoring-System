# 🚨 AI Powered Women Safety Monitoring System

An AI-based real-time women safety system that detects dangerous situations using Emotion Recognition and Weapon Detection.

---

## 📌 Project Overview

This project is designed to enhance women safety using Artificial Intelligence.  
The system detects:

- 🔪 Dangerous weapons (Knife, Scissors)
- 😨 Fearful or Sad facial expressions

When a threat is detected, the system:

- 🔊 Plays an alert sound
- ⚠ Displays a warning popup
- 📸 Captures screenshot
- 📩 Sends emergency SMS using Twilio
- 💾 Stores alert data in MongoDB

---

## 🛠 Technologies Used

- Python
- OpenCV
- YOLOv8 (Object Detection)
- Scikit-Learn (Emotion Detection)
- Tkinter (GUI)
- MongoDB
- Twilio API

---

## 🎯 Features

✔ Real-time camera monitoring  
✔ Weapon detection (Knife, Scissors)  
✔ Emotion detection (Fear, Sad)  
✔ Automatic alert system  
✔ Emergency contact notification  
✔ Screenshot capture  
✔ Database logging  
✔ User authentication system  

---

## 🧠 System Architecture

Camera → YOLO Model → Emotion Model → Threat Detection →  
Alert System → SMS Notification → Database Storage

---

## 📂 Project Structure

```
Women-Safety-Monitoring-System/
│
├── main.py
├── detection/
├── emotion_model.pkl
├── train_model.py
├── ui.py
├── database.py
├── weapon.yaml
├── requirements.txt
└── README.md
```

---

## ▶ How to Run the Project

1. Clone the repository:
```
git clone https://github.com/sneha123149/Women-Safety-Monitoring-System.git
```

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Run the application:
```
python main.py
```

---

## 🔐 Note

Sensitive credentials such as Twilio SID and Auth Token are not included for security reasons.

---

## 👩‍💻 Developed By

Sneha Dutta  
Diploma in Computer Science & Technology  
6th Semester Project  

---

## 🌟 Future Enhancements

- Mobile App Integration
- Live Location Sharing
- Cloud Deployment
- Improved Model Accuracy
- Multi-language Support

---
