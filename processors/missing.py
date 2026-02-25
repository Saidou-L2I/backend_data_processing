import numpy as np
import pandas as pd

def handle_missing(df, method="fill_mean", threshold=0.5):
    """
    Nettoie un DataFrame en gérant automatiquement les valeurs manquantes
    et en homogénéisant les colonnes catégorielles selon leur type majoritaire.

    Args:
        df (pd.DataFrame): DataFrame d'entrée
        method (str): Méthode pour remplir les colonnes numériques ["fill_mean", "fill_median", "drop"]
        threshold (float): Seuil pour supprimer une colonne trop vide (proportion NaN)

    Returns:
        pd.DataFrame: DataFrame nettoyé
    """
    df = df.copy()

    # 1️⃣ Uniformiser toutes les valeurs manquantes connues
    missing_values = ["--", "-", "n/a", "NA", "na", "N/A",
                      "", "null", "None", "#", "##", "###", "?", "*"]
    df.replace(missing_values, np.nan, inplace=True)

    # 2️⃣ Détection automatique type colonne
    for col in df.columns:
        numeric_version = pd.to_numeric(df[col], errors="coerce")
        numeric_count = numeric_version.notna().sum()
        total_count = df[col].notna().sum()

        if total_count == 0:
            continue

        if numeric_count / total_count > 0.8:
            # Colonne majoritairement numérique
            df[col] = numeric_version
        else:
            # Colonne catégorielle
            df[col] = df[col].astype("category")

            # Détecter la valeur majoritaire
            value_counts = df[col].value_counts()
            if not value_counts.empty:
                major_value = value_counts.idxmax()
                # Remplacer toutes les valeurs différentes par NaN
                df[col] = df[col].apply(lambda x: x if x == major_value else np.nan)

    # 3️⃣ Supprimer colonnes trop vides
    missing_ratio = df.isna().mean()
    df = df.loc[:, missing_ratio <= threshold]

    # 4️⃣ Séparer types
    num_cols = df.select_dtypes(include=[np.number]).columns
    cat_cols = df.select_dtypes(include=["category", "object"]).columns

    # 5️⃣ Remplissage numériques
    if method == "fill_mean":
        df[num_cols] = df[num_cols].fillna(df[num_cols].mean())
    elif method == "fill_median":
        df[num_cols] = df[num_cols].fillna(df[num_cols].median())
    elif method == "drop":
        df = df.dropna()

    # 6️⃣ Remplissage catégorielle par mode
    for col in cat_cols:
        mode = df[col].mode()
        if not mode.empty:
            df[col] = df[col].fillna(mode[0])

    return df