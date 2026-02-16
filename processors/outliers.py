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

        df_res[col] = df_res[col].apply(
            lambda x: lower if x < lower
            else upper if x > upper
            else x
        )

    return df_res