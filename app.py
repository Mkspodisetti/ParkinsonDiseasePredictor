import os
import numpy as np
import cv2
import logging
from flask import Flask, request, render_template, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
import pickle
import uuid
from models.spiral_model import analyze_spiral
from models.mri_model import analyze_mri
from models.symptoms_model import analyze_symptoms

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_key_for_development")

# Ensure upload directories exist
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
SPIRAL_FOLDER = os.path.join(UPLOAD_FOLDER, 'spirals')
MRI_FOLDER = os.path.join(UPLOAD_FOLDER, 'mri')

for folder in [UPLOAD_FOLDER, SPIRAL_FOLDER, MRI_FOLDER]:
    os.makedirs(folder, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Display the main page with the assessment form"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Process the uploaded files and questionnaire data"""
    try:
        # Generate a unique session ID
        session_id = str(uuid.uuid4())
        
        # Process spiral drawing
        spiral_result = None
        spiral_confidence = 0
        
        if 'spiral' in request.files:
            spiral_file = request.files['spiral']
            if spiral_file and spiral_file.filename and allowed_file(spiral_file.filename):
                # Save spiral file
                spiral_filename = secure_filename(f"{session_id}_{spiral_file.filename}")
                spiral_path = os.path.join(SPIRAL_FOLDER, spiral_filename)
                spiral_file.save(spiral_path)
                
                # Analyze spiral
                spiral_result, spiral_confidence = analyze_spiral(spiral_path)
                
                logging.debug(f"Spiral analysis result: {spiral_result}, confidence: {spiral_confidence}")
            else:
                flash("Please upload a valid spiral drawing image (png, jpg, jpeg, gif)", "danger")
                return redirect(url_for('index'))
        else:
            flash("Spiral drawing is required", "danger")
            return redirect(url_for('index'))
        
        # Process MRI scan (optional)
        mri_result = None
        mri_confidence = 0
        
        if 'mri' in request.files and request.files['mri'].filename:
            mri_file = request.files['mri']
            if mri_file and allowed_file(mri_file.filename):
                # Save MRI file
                mri_filename = secure_filename(f"{session_id}_{mri_file.filename}")
                mri_path = os.path.join(MRI_FOLDER, mri_filename)
                mri_file.save(mri_path)
                
                # Analyze MRI
                mri_result, mri_confidence = analyze_mri(mri_path)
                
                logging.debug(f"MRI analysis result: {mri_result}, confidence: {mri_confidence}")
        
        # Process symptom questionnaire
        symptoms = {
            'tremor': request.form.get('tremor', 'no'),
            'stiffness': request.form.get('stiffness', 'no'),
            'slowness': request.form.get('slowness', 'no'),
            'balance': request.form.get('balance', 'no'),
            'handwriting': request.form.get('handwriting', 'no'),
            'speech': request.form.get('speech', 'no'),
            'fatigue': request.form.get('fatigue', 'no')
        }
        
        symptoms_result, symptoms_confidence, urgent_consultation = analyze_symptoms(symptoms)
        logging.debug(f"Symptoms analysis result: {symptoms_result}, confidence: {symptoms_confidence}, urgent: {urgent_consultation}")
        
        # For prototype: We'll prioritize the symptom questionnaire result
        # but still include the other analyses for demonstration
        
        # Calculate dummy weights
        weights = {
            'spiral': 0.2,
            'mri': 0.1 if mri_result is not None else 0,
            'symptoms': 0.7 if mri_result is not None else 0.8
        }
        
        # Normalize weights
        total_weight = sum(weights.values())
        weights = {k: v/total_weight for k, v in weights.items()}
        
        # Calculate combined probability (mostly determined by symptoms)
        combined_probability = symptoms_confidence
        
        # Prepare results to display
        results = {
            'spiral': {
                'result': spiral_result,
                'confidence': spiral_confidence,
                'weight': weights['spiral']
            },
            'mri': {
                'result': mri_result,
                'confidence': mri_confidence if mri_result is not None else 0,
                'weight': weights['mri']
            },
            'symptoms': {
                'result': symptoms_result,
                'confidence': symptoms_confidence,
                'weight': weights['symptoms']
            },
            'combined_probability': combined_probability,
            'risk_level': get_risk_level(combined_probability),
            'urgent_consultation': urgent_consultation
        }
        
        return render_template('result.html', results=results)
        
    except Exception as e:
        logging.error(f"Error in prediction: {str(e)}")
        flash(f"An error occurred during analysis: {str(e)}", "danger")
        return redirect(url_for('index'))

def get_risk_level(probability):
    """Convert probability to risk level"""
    if probability < 0.2:
        return {"level": "Low", "class": "success"}
    elif probability < 0.5:
        return {"level": "Moderate", "class": "warning"}
    else:
        return {"level": "High", "class": "danger"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
