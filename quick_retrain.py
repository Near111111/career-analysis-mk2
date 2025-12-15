#!/usr/bin/env python3
"""
Simple script to retrain just the education model.
Uses only standard libraries and sklearn (already in your requirements).
"""

import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

print("=" * 60)
print("RETRAINING EDUCATION MODEL WITH FIELD SUPPORT")
print("=" * 60)

# Read the updated dataset
print("\n1. Loading education dataset...")
df = pd.read_csv('education_dataset.csv')
print(f"   ✓ Loaded {len(df)} programs")
print(f"   ✓ Columns: {list(df.columns)}")

# Check if field column exists
if 'field' not in df.columns:
    print("   ✗ ERROR: 'field' column not found in education_dataset.csv")
    print("   Make sure you have the updated dataset with field column.")
    exit(1)

print(f"   ✓ Field column found with {df['field'].nunique()} unique fields")

# Train the model
print("\n2. Training Random Forest model...")
# IMPORTANT: Include 'field' as a feature so the model uses it for predictions!
feature_cols = ["modality", "budget", "learning_style", "motivation", "field"]
target_col = "program_name"

X = df[feature_cols].copy()
y = df[target_col].copy()

# Encode features
encoders = {}
for col in X.columns:
    le = LabelEncoder()
    X[col] = X[col].fillna("").astype(str)
    X[col] = le.fit_transform(X[col])
    encoders[col] = le
    print(f"   ✓ Encoded '{col}': {len(le.classes_)} unique values")

# Encode target
y_le = LabelEncoder()
y = y.fillna("NA").astype(str)
y_enc = y_le.fit_transform(y)
print(f"   ✓ Encoded target: {len(y_le.classes_)} unique programs")

# Train model
print("\n3. Training with 400 trees...")
model = RandomForestClassifier(n_estimators=400, n_jobs=-1, random_state=42)
model.fit(X, y_enc)
print("   ✓ Model trained successfully")

# Save model
print("\n4. Saving model...")
joblib.dump({
    "model": model,
    "encoders": encoders,
    "target_encoder": y_le,
    "feature_cols": feature_cols,
    "raw_df": df  # This includes the 'field' column!
}, "model_education.pkl")
print("   ✓ Saved to model_education.pkl")

print("\n" + "=" * 60)
print("✅ SUCCESS! Education model retrained with field support")
print("=" * 60)
print("\nNow field_of_interest filtering will work correctly!")
print("Recommendations will be filtered by:")
print("  - Program Type (SHS, College, ALS, Graduate)")
print("  - Education Level")
print("  - Field of Interest (if selected)")
print("\nRestart your Flask app to use the new model.")
