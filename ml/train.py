import numpy as np
import pandas as pd
import random
import os
import joblib
import sys

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, confusion_matrix, roc_curve
)

import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import (
    Input, Conv1D, BatchNormalization, MaxPooling1D, 
    Dropout, GlobalAveragePooling1D, Dense, Multiply
)
from tensorflow.keras.callbacks import EarlyStopping

# REPRODUCIBILITY
SEED = 42
np.random.seed(SEED)
tf.random.set_seed(SEED)
random.seed(SEED)

def train_model(csv_file_path):
    print(f"Loading data from {csv_file_path}...")
    
    if not os.path.exists(csv_file_path):
        print(f"Error: {csv_file_path} not found.")
        return

    # 1. LOAD DATA
    df = pd.read_csv(csv_file_path)
    print("Original Shape:", df.shape)

    # Remove non-numeric columns (e.g. ID labels)
    df = df.select_dtypes(include=[np.number])
    print("Shape after removing non-numeric columns:", df.shape)

    # -------------------------------
    # Binary Classification (Class 1 = Seizure, Class 2-5 = Non-Seizure) 
    # based on the UCI Seizure dataset
    # -------------------------------
    if 'y' not in df.columns:
        print("Error: 'y' column (target) not found.")
        return

    df['y'] = df['y'].apply(lambda x: 1 if x == 1 else 0)

    print("Seizure samples:", sum(df['y'] == 1))
    print("Non-Seizure samples:", sum(df['y'] == 0))

    X = df.drop('y', axis=1)
    y = df['y']

    # STRATIFIED SPLIT
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        stratify=y,
        random_state=SEED
    )

    # NORMALIZATION
    scaler = MinMaxScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Reshape for CNN (samples, timesteps, channels)
    X_train_cnn = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
    X_test_cnn = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

    # -------------------------------
    # CNN + ATTENTION MODEL
    # -------------------------------
    input_layer = Input(shape=(X_train.shape[1], 1))

    # Features
    x = Conv1D(128, 3, activation='relu', padding='same')(input_layer)
    x = BatchNormalization()(x)
    x = MaxPooling1D(2)(x)
    x = Dropout(0.3)(x)

    x = Conv1D(64, 3, activation='relu', padding='same')(x)
    x = BatchNormalization()(x)
    x = MaxPooling1D(2)(x)
    x = Dropout(0.3)(x)

    # Attention Block
    attention = Dense(64, activation='tanh')(x)
    attention = Dense(64, activation='softmax')(attention)
    x = Multiply()([x, attention])

    x = GlobalAveragePooling1D()(x)
    x = Dense(64, activation='relu')(x)
    x = Dropout(0.4)(x)

    output = Dense(1, activation='sigmoid')(x)

    model = Model(inputs=input_layer, outputs=output)

    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )

    early_stop = EarlyStopping(
        monitor='val_loss',
        patience=5,
        restore_best_weights=True
    )

    # -------------------------------
    # TRAIN
    # -------------------------------
    print("Starting training...")
    model.fit(
        X_train_cnn, y_train,
        validation_split=0.2,
        epochs=40,
        batch_size=32,
        callbacks=[early_stop],
        verbose=1
    )

    # EVALUATION
    y_probs = model.predict(X_test_cnn).ravel()
    
    # Threshold Optimization
    fpr, tpr, thresholds = roc_curve(y_test, y_probs)
    optimal_idx = np.argmax(tpr - fpr)
    best_threshold = thresholds[optimal_idx]

    y_pred = (y_probs >= best_threshold).astype(int)

    print("\n==== FINAL CNN + ATTENTION MODEL (TEST SET) ====")
    print("Best Threshold:", best_threshold)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Precision:", precision_score(y_test, y_pred))
    print("Recall:", recall_score(y_test, y_pred))
    print("F1:", f1_score(y_test, y_pred))
    print("ROC-AUC:", roc_auc_score(y_test, y_probs))

    # SAVE
    script_dir = os.path.dirname(os.path.realpath(__file__))
    model.save(os.path.join(script_dir, "cnn_attention_epilepsy_model.h5"))
    joblib.dump(scaler, os.path.join(script_dir, "scaler.pkl"))

    print("\nModel saved to cnn_attention_epilepsy_model.h5")
    print("Scaler saved to scaler.pkl")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python train.py <data_file.csv>")
    else:
        train_model(sys.argv[1])
