import os
import random
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)


def analyze_mri(image_path):
    """
    Mock analyze an MRI scan for Parkinson's detection based on filename

    Args:
        image_path: Path to the MRI scan image

    Returns:
        tuple: (prediction result, confidence score)
    """
    try:
        filename = os.path.basename(image_path).lower()

        if "healthy" in filename:
            result = "Negative"
            confidence = round(random.uniform(0.1, 0.2), 2)

        elif "patient" in filename:
            result = "Positive"
            confidence = round(random.uniform(0.8, 1.0), 2)

        else:
            result = "Borderline"
            confidence = round(random.uniform(0.5, 0.65), 2)

        logging.debug(
            f"Filename-based MRI mock prediction: {result}, confidence: {confidence}"
        )
        return result, confidence

    except Exception as e:
        logging.error(f"Error in mock MRI analysis: {str(e)}")
        return "Error in analysis", 0.5
