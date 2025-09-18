import os
import logging
import joblib
import numpy as np
from skimage.io import imread
from skimage.color import rgb2gray
from skimage.transform import resize

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Load the trained model
try:
    model = joblib.load("mri.pkl")  # Ensure this file exists
    logging.info("MRI model loaded successfully.")
except Exception as e:
    logging.error(f"Failed to load MRI model: {e}")
    model = None


def extract_mri_features(image_path):
    """
    Extract features from MRI image for prediction (grayscale resize and flatten).

    Args:
        image_path: Path to MRI image

    Returns:
        np.ndarray: Flattened image vector
    """
    try:
        image = imread(image_path)
        image = rgb2gray(image)
        image = resize(image, (128, 128))
        return image.flatten()
    except Exception as e:
        logging.error(f"Failed to extract MRI features: {e}")
        return None


def analyze_mri(image_path):
    """
    Analyze MRI image using a trained model.

    Args:
        image_path: Path to MRI image

    Returns:
        tuple: (prediction result, confidence score)
    """
    if model is None:
        return "Model not loaded", 0.0

    features = extract_mri_features(image_path)
    if features is None:
        return "Failed to extract MRI features", 0.0

    try:
        prediction = model.predict([features])[0]
        proba = model.predict_proba([features])[0]

        label = "Positive" if prediction == 1 else "Negative"
        confidence = round(np.max(proba), 2)

        logging.debug(f"MRI prediction: {label}, confidence: {confidence}")
        return label, confidence

    except Exception as e:
        logging.error(f"Error during MRI prediction: {e}")
        return "Prediction error", 0.5
