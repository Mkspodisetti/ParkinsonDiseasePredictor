import os
import logging
import joblib
import numpy as np
from skimage.io import imread
from skimage.color import rgb2gray
from skimage.transform import resize
from skimage.feature import hog

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Load the pre-trained model
try:
    model = joblib.load("spiral.pkl")
    logging.info("Model loaded successfully.")
except Exception as e:
    logging.error(f"Failed to load model: {e}")
    model = None


def extract_features(image_path):
    """
    Extract features (HOG) from the image for prediction.

    Args:
        image_path: Path to the spiral drawing image

    Returns:
        np.ndarray: Extracted feature vector
    """
    try:
        image = imread(image_path)
        image = rgb2gray(image)  # Convert to grayscale
        image = resize(image, (128, 128))  # Resize to fixed size
        features, _ = hog(image,
                          pixels_per_cell=(8, 8),
                          cells_per_block=(2, 2),
                          visualize=True,
                          feature_vector=True)
        return features
    except Exception as e:
        logging.error(f"Feature extraction failed: {e}")
        return None


def analyze_spiral(image_path):
    """
    Analyze a spiral drawing image using the trained model.

    Args:
        image_path: Path to the spiral drawing image

    Returns:
        tuple: (prediction result, confidence score)
    """
    if model is None:
        return "Model not loaded", 0.0

    features = extract_features(image_path)
    if features is None:
        return "Failed to extract features", 0.0

    try:
        prediction = model.predict([features])[0]
        proba = model.predict_proba([features])[0]

        # Assuming "Positive" = Parkinson's, "Negative" = Healthy
        label = "Positive" if prediction == 1 else "Negative"
        confidence = round(np.max(proba), 2)

        logging.debug(f"Model prediction: {label}, confidence: {confidence}")
        return label, confidence

    except Exception as e:
        logging.error(f"Prediction error: {e}")
        return "Error during prediction", 0.5
