import numpy as np
import pandas as pd


def handle_missing(df, method="fill_mean", threshold=0.5, categorical_override=None):
    """
    Nettoie un DataFrame en gérant les valeurs manquantes et la conversion texte ↔ numérique.

    Args:
        df (pd.DataFrame): DataFrame d'entrée
        method (str): méthode pour traiter les colonnes numériques ["fill_mean", "fill_median", "drop"]
        threshold (float): seuil de valeurs manquantes pour supprimer une colonne
        categorical_override (list): colonnes à toujours traiter comme catégorielles

    Returns:
        pd.DataFrame: DataFrame nettoyé
    """

    if categorical_override is None:
        categorical_override = []

    df = df.copy()

    # 1️⃣ Uniformiser toutes les valeurs manquantes connues
    missing_values = [
        "--", "-", "n/a", "NA", "na", "N/A",
        "", "null", "None",
        "#", "##", "###",
        "?", "*"
    ]
    df.replace(missing_values, np.nan, inplace=True)

    # 2️⃣ Détecter le type dominant colonne par colonne
    for col in df.columns:

        # Forcer certaines colonnes à rester catégorielles
        if col in categorical_override:
            df[col] = df[col].astype(str)
            df.loc[df[col].isin(["nan", "NaN"]), col] = np.nan
            continue

        # Tentative conversion numérique
        numeric_version = pd.to_numeric(df[col], errors="coerce")
        numeric_count = numeric_version.notna().sum()
        total_count = df[col].notna().sum()

        if total_count == 0:
            continue

        # Colonne numérique seulement si la majorité est très numérique
        if numeric_count / total_count > 0.8:  # seuil plus strict
            df[col] = numeric_version
        else:
            # Sinon colonne catégorielle
            df[col] = df[col].astype(str)
            df.loc[df[col].isin(["nan", "NaN"]), col] = np.nan

    # 3️⃣ Supprimer colonnes trop vides
    missing_ratio = df.isna().mean()
    df = df.loc[:, missing_ratio <= threshold]

    # 4️⃣ Séparer types
    num_cols = df.select_dtypes(include=[np.number]).columns
    cat_cols = df.select_dtypes(exclude=[np.number]).columns

    # 5️⃣ Traitement colonnes numériques
    if method == "fill_mean":
        df[num_cols] = df[num_cols].fillna(df[num_cols].mean())
    elif method == "fill_median":
        df[num_cols] = df[num_cols].fillna(df[num_cols].median())
    elif method == "drop":
        df = df.dropna()

    # 6️⃣ Traitement colonnes catégorielles
    for col in cat_cols:
        mode = df[col].mode()
        df[col] = df[col].fillna(mode[0] if not mode.empty else "Inconnu")

    return df
