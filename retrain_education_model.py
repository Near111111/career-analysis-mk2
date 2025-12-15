#!/usr/bin/env python3
# Quick script to retrain just the education model with the new field feature

import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

def train_pack(csv_path, model_path, feature_cols, target_col):
    """Train and save ML model"""
    df = pd.read_csv(csv_path)
    
    # Ensure feature_cols present
    if not feature_cols:
        feature_cols = [c for c in df.columns if c != target_col]
    
    X = df[feature_cols].copy()
    y = df[target_col].copy()

    encoders = {}
    for col in X.columns:
        le = LabelEncoder()
        X[col] = X[col].fillna("NA").astype(str)
        X[col] = le.fit_transform(X[col])
        encoders[col] = le

    y_le = LabelEncoder()
    y = y.fillna("NA").astype(str)
    y_enc = y_le.fit_transform(y)

    model = RandomForestClassifier(n_estimators=400, n_jobs=-1, random_state=42)
    model.fit(X, y_enc)

    # Save model with metadata
    joblib.dump({
        "model": model,
        "encoders": encoders,
        "target_encoder": y_le,
        "feature_cols": feature_cols,
        "raw_df": df
    }, model_path)

    print(f"✅ Trained and saved {model_path}")
    print(f"   Features: {feature_cols}")
    print(f"   Target: {target_col}")
    print(f"   Dataset size: {len(df)} rows")

if __name__ == "__main__":
    print("Retraining education model with field feature...")
    train_pack(
        "education_dataset.csv", 
        "model_education.pkl",
        ["modality","budget","learning_style","motivation","field"], 
        "program_name"
    )
    print("\n✨ Education model retrained successfully!")
    print("Now field_of_interest filter will work properly.")
