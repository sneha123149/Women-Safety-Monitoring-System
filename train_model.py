from sklearn.linear_model import LogisticRegression
import joblib
import numpy as np
import os

# All 6 dummy emotion labels
emotions = ["fear","sad"]

# Create 10 random samples for each emotion
X = []
y = []
for emotion in emotions:
    for _ in range(10):
        X.append(np.random.rand(48 * 48))
        y.append(emotion)

X = np.array(X)

# Train dummy model
model = LogisticRegression(max_iter=1000)
model.fit(X, y)

# Save model in the project root folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "emotion_model.pkl")

joblib.dump(model, MODEL_PATH)

print(f"✅ Dummy model trained with {len(X)} samples and saved as '{MODEL_PATH}'")
