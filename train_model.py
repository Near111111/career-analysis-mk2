# train_and_save_models.py
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

def train_pack(csv_path, model_path, feature_cols, target_col):
    df = pd.read_csv(csv_path)
    # Ensure feature_cols present; if not infer all except target
    if not feature_cols:
        feature_cols = [c for c in df.columns if c != target_col]
    X = df[feature_cols].copy()
    y = df[target_col].copy()

    encoders = {}
    for col in X.columns:
        le = LabelEncoder()
        # fill na and convert to str to keep consistent
        X[col] = X[col].fillna("NA").astype(str)
        X[col] = le.fit_transform(X[col])
        encoders[col] = le

    y_le = LabelEncoder()
    y = y.fillna("NA").astype(str)
    y_enc = y_le.fit_transform(y)

    model = RandomForestClassifier(n_estimators=400, n_jobs=-1, random_state=42)
    model.fit(X, y_enc)

    # Save also the raw metadata for mapping predictions to full rows
    joblib.dump({
        "model": model,
        "encoders": encoders,
        "target_encoder": y_le,
        "feature_cols": feature_cols,
        "raw_df": df
    }, model_path)

    print("Saved", model_path)

# Career: target = job_title, features = primary_skills,industry,salary,work_environment
train_pack("career_dataset.csv", "model_career.pkl",
           ["primary_skills","industry","salary","work_environment"], "job_title")

# Education: target = program_name
# IMPORTANT: field is now a FEATURE so model predictions are based on user's field selection
train_pack("education_dataset.csv", "model_education.pkl",
           ["modality","budget","learning_style","motivation","field"], "program_name")

# TESDA
train_pack("tesda_dataset.csv", "model_tesda.pkl",
           ["budget","time_available","location","experience"], "course_name")
