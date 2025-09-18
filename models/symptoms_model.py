import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def analyze_symptoms(symptoms):
    """
    Analyze symptom questionnaire data for Parkinson's detection
    
    Args:
        symptoms: Dictionary of symptom responses
        
    Returns:
        tuple: (prediction result, confidence score)
    """
    try:
        # Count the number of "yes" answers
        yes_count = 0
        total_questions = 0
        
        for symptom, response in symptoms.items():
            total_questions += 1
            if response.lower() == 'yes':
                yes_count += 1
        
        # For prototype: 3 or more "yes" answers indicates potential Parkinson's
        if yes_count >= 3:
            result = "Positive"
            # Scale confidence based on number of "yes" answers
            confidence = min(1.0, yes_count / total_questions)
        else:
            result = "Negative"
            # Scale confidence inversely
            confidence = max(0.0, 1.0 - (yes_count / total_questions))
        
        # Calculate urgency level for doctor consultation
        urgent_consultation = (yes_count >= total_questions - 1)
        
        logging.debug(f"Symptoms analysis - yes count: {yes_count}/{total_questions}, confidence: {confidence}, urgent: {urgent_consultation}")
        return result, confidence, urgent_consultation
        
    except Exception as e:
        logging.error(f"Error analyzing symptoms: {str(e)}")
        # Return a conservative result in case of error
        return "Error in analysis", 0.5, False
