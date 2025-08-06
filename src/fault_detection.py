# Signal Analysis & Fault Detection Module
# Contains algorithms for signal analysis and fault detection

import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

def analyze_signals(data):
    """
    Preprocesses and normalizes PCB data for analysis.
    Returns normalized features and labels (if present).
    """
    features = data.drop(columns=[col for col in ['sample_id', 'faulty'] if col in data.columns], errors='ignore')
    scaler = StandardScaler()
    X = scaler.fit_transform(features)
    y = data['faulty'] if 'faulty' in data.columns else None
    return X, y

def detect_faults(X, y=None):
    """
    Detects faults using a simple logistic regression model.
    If labels are provided, trains and evaluates the model.
    If not, predicts faults on new data.
    Returns predictions and (if y is given) accuracy.
    """
    model = LogisticRegression()
    if y is not None:
        model.fit(X, y)
        preds = model.predict(X)
        accuracy = np.mean(preds == y)
        return preds, accuracy
    else:
        # For predictions without training, use a threshold-based approach
        # This is a simplified model for demonstration purposes
        # In production, use a pre-trained model loaded from disk
        
        # Define acceptable ranges for PCB parameters
        threshold_values = {
            'voltage': (4.8, 5.2),    # acceptable voltage range
            'current': (0.08, 0.12),  # acceptable current range
            'resistance': (45, 55)    # acceptable resistance range
        }
        
        # Calculate statistics for the sample
        # Using standardized data, we need to invert the standardization
        # In a real scenario, we would store the scaler and use it to transform back
        # For simplicity, we'll use a basic threshold on the standardized data
        
        # If any value is > 2 standard deviations from mean, mark as faulty
        anomaly_scores = np.sum(np.abs(X) > 2.0, axis=1)
        preds = (anomaly_scores > 0).astype(int)
        
        return preds
