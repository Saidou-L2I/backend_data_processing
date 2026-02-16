import numpy as np

def handle_missing(df, method="fill_mean", threshold=0.5):
    df = df.copy()

    # 1️⃣ Supprimer colonnes avec trop de valeurs manquantes
    missing_ratio = df.isna().mean()
    cols_to_drop = missing_ratio[missing_ratio > threshold].index
    df = df.drop(columns=cols_to_drop)

    # 2️⃣ Séparer numériques et catégorielles
    num_cols = df.select_dtypes(include=[np.number]).columns
    cat_cols = df.select_dtypes(exclude=[np.number]).columns

    # 3️⃣ Traitement des numériques
    if method == "fill_mean":
        df[num_cols] = df[num_cols].fillna(df[num_cols].mean())
    elif method == "fill_median":
        df[num_cols] = df[num_cols].fillna(df[num_cols].median())
    elif method == "drop":
        df = df.dropna()

    # 4️⃣ Traitement des catégorielles
    for col in cat_cols:
        mode = df[col].mode()
        df[col] = df[col].fillna(mode[0] if not mode.empty else "Inconnu")

    return df