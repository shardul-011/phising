import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from src.utils import print_header, ensure_artifacts_dir

def preprocess_data(df, target_col, test_size, random_state, scaler_path):
    print_header("PREPROCESSING DATA")
    df.columns = df.columns.str.strip()

    if target_col not in df.columns:
        raise KeyError(
            f"Target column '{target_col}' not found.\n"
            f"Available columns: {df.columns.tolist()}"
        )


    df[target_col] = df[target_col].map({-1: 0, 1: 1})

    X = df.drop(target_col, axis=1)
    y = df[target_col]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Create artifacts directory properly
    ensure_artifacts_dir(os.path.dirname(scaler_path))

    # Save scaler
    joblib.dump(scaler, scaler_path)
    print(f"Scaler saved → {scaler_path}")

    return X_train_scaled, X_test_scaled, y_train, y_test