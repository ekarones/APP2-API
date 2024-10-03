import numpy as np
import sqlite3
from joblib import load
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array

IMG_HEIGHT, IMG_WIDTH = 256, 256
diseases = [
    "Black Rot (Pudrición Negra)",
    "Healthy (Saludable)",
    "Cedar Rust (Roya del Cedro y Manzano)",
    "Scab (Sarna del Manzano)",
]
feature_extractor = load_model("models/feature_extractor_cnn.h5")
pca_model = load("models/pca_model.joblib")
svm_model = load("models/svm_model.joblib")


def predict_img(img_path):
    image = load_img(img_path, target_size=(IMG_HEIGHT, IMG_WIDTH))
    image = img_to_array(image) / 255.0
    images = list()
    images.append(image)
    images = np.array(images)
    features = feature_extractor.predict(images)
    features_scaled = pca_model.transform(features)
    result = svm_model.predict(features_scaled)
    print(diseases[result[0]])

    conn = sqlite3.connect("database/app-db.sqlite")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name, description FROM diseases WHERE name = ?", (diseases[result[0]],)
    )
    result = cursor.fetchone()
    conn.close()
    if result:
        name, description = result
        return name, description
    else:
        return None, None
