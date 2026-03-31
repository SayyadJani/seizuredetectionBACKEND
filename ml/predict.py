import sys
import numpy as np
import pandas as pd
import joblib
import json
import os

# Suppress TensorFlow logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import tensorflow as tf

def predict_seizure(file_path):
    try:
        # 1. Load the Scaler and Model
        # Paths are relative to the script's location
        script_dir = os.path.dirname(os.path.realpath(__file__))
        scaler_path = os.path.join(script_dir, "scaler.pkl")
        model_path = os.path.join(script_dir, "cnn_attention_epilepsy_model.h5")

        if not os.path.exists(scaler_path) or not os.path.exists(model_path):
            return {"error": "Model files (scaler.pkl or cnn_attention_epilepsy_model.h5) not found. Run train.py first."}

        scaler = joblib.load(scaler_path)
        model = tf.keras.models.load_model(model_path)

        # 2. Load the input data
        # Check if file exists
        if not os.path.exists(file_path):
            return {"error": f"Input file not found: {file_path}"}

        df = pd.read_csv(file_path)

        # Preprocess input data
        # We need to drop ID columns or anything non-numeric, similar to training
        df = df.select_dtypes(include=[np.number])
        
        # If 'y' column (labels) is present, drop it
        if 'y' in df.columns:
            df = df.drop('y', axis=1)
        
        # We only want the first row for a single prediction, or all rows?
        # Let's predict for all rows and return the summary
        X = scaler.transform(df)
        X = X.reshape(X.shape[0], X.shape[1], 1)

        # 3. Predict
        probs = model.predict(X, verbose=0).ravel()
        
        # Optimization: Average probability across many readings, or find if ANY reading is seizure
        # Usually for this dataset, each row is a time window.
        # Optimized Clinical Threshold from Training (Best Threshold = 0.1659)
        THRESHOLD = 0.166 
        
        preds = (probs >= THRESHOLD).astype(int)
        
        # Calculate summary
        seizure_count = int(np.sum(preds))
        total_count = len(preds)
        
        # In medicine, if spike incidence is > 5%, we classify as risk
        is_seizure = (seizure_count / total_count) > 0.05 
        
        # Max probability often reflects the "spike" better in clinical settings
        max_prob = float(np.max(probs))
        avg_prob = float(np.mean(probs))

        return {
            "seizure": bool(is_seizure),
            "confidence": max_prob if is_seizure else avg_prob,
            "seizure_count": seizure_count,
            "total_readings": total_count,
            "predictions_list": preds.tolist()
        }

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No file path provided."}))
    else:
        file_path = sys.argv[1]
        result = predict_seizure(file_path)
        print(json.dumps(result))
