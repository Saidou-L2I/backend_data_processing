"""import numpy as np
import pandas as pd

def handle_missing(df, method="fill_mean", threshold=0.5):
    #
    Nettoie un DataFrame en gérant automatiquement les valeurs manquantes
    et en remplissant les colonnes catégorielles par leur mode.
    Les valeurs aberrantes (types différents) dans les colonnes catégorielles
    sont remplacées par NaN avant le remplissage.
    #
    df = df.copy()

    # 1️⃣ Uniformiser valeurs manquantes
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

            # Détecter les types aberrants : garder seulement les str existants
            df[col] = df[col].apply(lambda x: x if isinstance(x, str) else np.nan)

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

    return df"""
##########"
import numpy as np
import pandas as pd


def is_categorical_numeric(col, threshold_unique=0.05, max_unique=20):
    """
    Détecte si une colonne numérique est en réalité catégorielle
    (ex: 0/1, codes produits)
    """
    unique_count = col.nunique()
    total_count = len(col)

    if unique_count <= max_unique or (unique_count / total_count) < threshold_unique:
        return True
    return False


def is_probable_id(col):
    """
    Détecte une colonne ID (valeurs uniques)
    """
    return col.nunique() == len(col)


def handle_missing_ultimate(
    df,
    method="fill_mean",
    threshold=0.5,
    dominance_ratio=0.7
):
    """
    Nettoyage avancé intelligent :
    - Détection type dominant
    - Gestion colonnes mixtes
    - Détection numériques catégoriels
    - Protection ID
    - Remplissage intelligent
    """

    df = df.copy()

    # 🔥 1️⃣ Uniformiser valeurs manquantes
    missing_values = [
        "--", "-", "n/a", "NA", "na", "N/A",
        "", "null", "None", "#", "##", "###", "?", "*"
    ]
    df.replace(missing_values, np.nan, inplace=True)

    # 🔥 2️⃣ Détection intelligente colonnes
    for col in df.columns:
        col_data = df[col]

        # 🔥 ignorer colonne vide
        if col_data.notna().sum() == 0:
            continue

        # 🔥 détecter ID → ne pas toucher
        if is_probable_id(col_data):
            continue

        numeric_version = pd.to_numeric(col_data, errors="coerce")

        numeric_count = numeric_version.notna().sum()
        total_count = col_data.notna().sum()

        ratio = numeric_count / total_count

        # =========================
        # 🔥 CAS NUMÉRIQUE DOMINANT
        # =========================
        if ratio >= dominance_ratio:
            df[col] = numeric_version

            # 🔥 vérifier si c’est catégoriel déguisé
            if is_categorical_numeric(df[col]):
                df[col] = df[col].astype("object")

        # =========================
        # 🔥 CAS CATEGORIEL DOMINANT
        # =========================
        else:
            df[col] = col_data.astype(str)

            # supprimer valeurs aberrantes
            df[col] = df[col].apply(
                lambda x: x if isinstance(x, str) else np.nan
            )

            df[col] = df[col].str.strip()

    # 🔥 3️⃣ Supprimer colonnes trop vides
    missing_ratio = df.isna().mean()
    df = df.loc[:, missing_ratio <= threshold]

    # 🔥 4️⃣ Séparer types
    num_cols = df.select_dtypes(include=[np.number]).columns
    cat_cols = df.select_dtypes(include=["object"]).columns

    # 🔥 5️⃣ Nettoyage final numérique
    for col in num_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # 🔥 6️⃣ Remplissage numérique
    if method == "fill_mean":
        df[num_cols] = df[num_cols].fillna(df[num_cols].mean())

    elif method == "fill_median":
        df[num_cols] = df[num_cols].fillna(df[num_cols].median())

    elif method == "drop":
        df = df.dropna()

    # 🔥 7️⃣ Remplissage catégoriel (mode)
    for col in cat_cols:
        mode = df[col].mode()
        if not mode.empty:
            df[col] = df[col].fillna(mode[0])

    return df