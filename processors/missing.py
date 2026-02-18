import numpy as np
import pandas as pd

def handle_missing(df, method="fill_mean", threshold=0.5, categorical_override=None):
    """
    Nettoie un DataFrame en gérant les valeurs manquantes et en traitant correctement
    les colonnes numériques et catégorielles.

    Args:
        df (pd.DataFrame): DataFrame d'entrée
        method (str): Méthode pour remplir les colonnes numériques ["fill_mean", "fill_median", "drop"]
        threshold (float): Seuil pour supprimer une colonne trop vide (proportion NaN)
        categorical_override (list): Liste de colonnes à toujours considérer comme catégorielles

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

    # 2️⃣ Détection type dominant colonne par colonne
    for col in df.columns:

        if col in categorical_override:
            # Forcer colonne catégorielle
            df[col] = df[col].astype(str)
            df.loc[df[col].isin(["nan", "NaN"]), col] = np.nan
            continue

        # Tentative conversion numérique
        numeric_version = pd.to_numeric(df[col], errors="coerce")
        numeric_count = numeric_version.notna().sum()
        total_count = df[col].notna().sum()

        if total_count == 0:
            continue

        # Colonne majoritairement numérique (>80%)
        if numeric_count / total_count > 0.8:
            df[col] = numeric_version
        else:
            # Colonne catégorielle
            df[col] = df[col].astype(str)
            df.loc[df[col].isin(["nan", "NaN"]), col] = np.nan

            # Remplacer les "valeurs invalides" par NaN
            # Exemple : on considère valide toutes les valeurs observées >1 occurrence
            value_counts = df[col].value_counts()
            valid_values = value_counts.index.tolist()
            df[col] = df[col].apply(lambda x: x if x in valid_values else np.nan)

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
