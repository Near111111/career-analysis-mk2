import joblib
import numpy as np
import pandas as pd

class MLModel:
    def __init__(self):
        self.models = {}  # pathway -> pack dict

    def load_all(self):
        for key in ["career","education","tesda"]:
            path = f"model_{key}.pkl"
            try:
                pack = joblib.load(path)
                self.models[key] = pack
                print("Loaded", path)
            except Exception as e:
                print("Could not load", path, e)

    def predict_top_k(self, pathway, input_dict, k=10):
        """
        input_dict: raw fields matching feature_cols stored in pack
        returns: list of dicts: {title, match, metadata_row}
        """
        if pathway not in self.models:
            return []

        pack = self.models[pathway]
        model = pack["model"]
        encoders = pack["encoders"]
        target_enc = pack["target_encoder"]
        feature_cols = pack["feature_cols"]
        raw_df = pack["raw_df"]

        # build X row in correct order
        row = []
        for col in feature_cols:
            val = input_dict.get(col, "")
            # ensure consistent string type as used in training
            val = str(val if val is not None else "")
            le = encoders[col]
            # if unseen value, attempt to handle: add as new label by mapping to -1 (we'll map to most common)
            if val in le.classes_:
                encoded = int(le.transform([val])[0])
            else:
                # fallback: encode as most frequent class (index 0)
                encoded = 0
            row.append(encoded)

        X = np.array(row).reshape(1, -1)
        probs = model.predict_proba(X)[0]  # probabilities for each target class
        top_idx = np.argsort(probs)[::-1][:k]

        results = []
        for idx in top_idx:
            label = target_enc.inverse_transform([idx])[0]
            match_score = round(float(probs[idx]) * 100, 1)  # e.g., 92.4
            # get first matching row metadata by label (search last column which is the target)
            target_col = raw_df.columns[-1]
            meta_row = raw_df[raw_df[target_col].astype(str) == str(label)].head(1)
            meta = meta_row.to_dict(orient="records")[0] if not meta_row.empty else {}
            results.append({
                "title": str(label),
                "match": match_score,
                "metadata": meta
            })

        return results
