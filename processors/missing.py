import numpy as np
import pandas as pd

def handle_missing(df, method="fill_mean", threshold=0.5):

    df = df.copy()

    # 1️⃣ Uniformiser valeurs manquantes connues
    missing_values = [
        "--", "-", "n/a", "NA", "na", "N/A",
        "", "null", "None",
        "#", "##", "###",
        "?", "*"
    ]
    df.replace(missing_values, np.nan, inplace=True)

    # 2️⃣ Détection type dominant colonne par colonne
    for col in df.columns:

        # Tentative conversion numérique
        numeric_version = pd.to_numeric(df[col], errors="coerce")

        numeric_count = numeric_version.notna().sum()
        total_count = df[col].notna().sum()

        if total_count == 0:
            continue

        # Si majorité numérique → considérer comme numérique
        if numeric_count / total_count > 0.5:
            df[col] = numeric_version  # tout ce qui n'est pas numérique devient NaN
        else:
            # Sinon colonne catégorielle → convertir tout en string
            df[col] = df[col].astype(str)
            df.loc[df[col] == "nan", col] = np.nan

    # 3️⃣ Supprimer colonnes trop vides
    missing_ratio = df.isna().mean()
    df = df.loc[:, missing_ratio <= threshold]

    # 4️⃣ Séparer types
    num_cols = df.select_dtypes(include=[np.number]).columns
    cat_cols = df.select_dtypes(exclude=[np.number]).columns

    # 5️⃣ Traitement numériques
    if method == "fill_mean":
        df[num_cols] = df[num_cols].fillna(df[num_cols].mean())

    elif method == "fill_median":
        df[num_cols] = df[num_cols].fillna(df[num_cols].median())

    elif method == "drop":
        df = df.dropna()

    # 6️⃣ Traitement catégorielles
    for col in cat_cols:
        mode = df[col].mode()
        df[col] = df[col].fillna(mode[0] if not mode.empty else "Inconnu")

    return df
