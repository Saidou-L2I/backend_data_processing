import numpy as np

def handle_outliers_smart(df):
    df_res = df.copy()
    num_cols = df.select_dtypes(include=[np.number]).columns

    for col in num_cols:
        Q1 = df_res[col].quantile(0.25)
        Q3 = df_res[col].quantile(0.75)
        IQR = Q3 - Q1

        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        # Remplacer les valeurs hors bornes par lower ou upper
        df_res[col] = np.clip(df_res[col], lower, upper)

    return df_res