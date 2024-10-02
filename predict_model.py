import numpy as np
from joblib import load
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array

IMG_HEIGHT, IMG_WIDTH = 256, 256
diseases = ["Black Rot", "Healthy", "Cedar Rust", "Scab"]
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
    return diseases[result[0]]
