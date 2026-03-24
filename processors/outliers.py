"""import numpy as np
#import pandas as pd
def handle_outliers_smart(df):
    df_res = df.copy()
    num_cols = df_res.select_dtypes(include=[np.number]).columns

    for col in num_cols:
        # 🔥 1️⃣ Supprimer les valeurs négatives AVANT calcul
        df_res.loc[df_res[col] < 0, col] = np.nan

        # 🔥 2️⃣ Calculer les statistiques sans les négatifs
        Q1 = df_res[col].quantile(0.25)
        Q3 = df_res[col].quantile(0.75)
        IQR = Q3 - Q1

        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        median = df_res[col].median()

        # 🔥 3️⃣ Détecter les outliers
        mask = (df_res[col] < lower) | (df_res[col] > upper)

        # 🔥 4️⃣ Remplacer outliers ET négatifs par médiane
        df_res.loc[mask, col] = median
        df_res[col].fillna(median, inplace=True)

    return df_res"""


import numpy as np
import pandas as pd

def handle_outliers_smart(df, iqr_factor=1.5):
    """
    Nettoyage des outliers via clipping IQR (inclut négatifs automatiquement).

    Parameters
    ----------
    df : pd.DataFrame
    iqr_factor : float
        Facteur IQR pour définir les bornes.

    Returns
    -------
    pd.DataFrame
    """
    df_res = df.copy()
    num_cols = df_res.select_dtypes(include=[np.number]).columns

    for col in num_cols:
        col_data = df_res[col].dropna()
        if col_data.empty:
            continue  # éviter erreurs sur colonnes vides

        Q1 = col_data.quantile(0.25)
        Q3 = col_data.quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - iqr_factor * IQR
        upper = Q3 + iqr_factor * IQR

        df_res[col] = df_res[col].clip(lower=lower, upper=upper)

    return df_res