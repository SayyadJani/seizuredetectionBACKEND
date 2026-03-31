# ML Model Integration

This directory contains the Python scripts for the Epileptic Seizure Detection model.

## Setup

1. **Install Python**: Ensure you have Python 3.8+ installed.
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Workflow

### 1. Training the Model
To generate the model files (`cnn_attention_epilepsy_model.h5` and `scaler.pkl`), you must run the training script with your dataset:
```bash
python train.py "Epileptic Seizure Recognition.csv"
```
*Note: Make sure your CSV file is in the same directory or provide the full path.*

### 2. Prediction
The Node.js backend uses `predict.py` to get results. 
- It loads the generated `.h5` and `.pkl` files.
- It expects an EEG dataset CSV as input.
- It returns a JSON object with the prediction results.

## Troubleshooting

- If the backend fails to find `python`, ensure it's in your system PATH.
- If you use `python3`, update the `spawn("python", ...)` command in `controllers/predictionController.js`.
- Ensure the `uploads` folder exists in the backend root directory.
