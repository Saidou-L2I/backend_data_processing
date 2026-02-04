import numpy as np

def handle_outliers_smart(df):
    df_res = df.copy()
    num_cols = df.select_dtypes(include=[np.number]).columns

    for col in num_cols:
        Q1, Q3 = df_res[col].quantile(0.25), df_res[col].quantile(0.75)
        IQR = Q3 - Q1
        mask = (df_res[col] < (Q1 - 1.5 * IQR)) | (df_res[col] > (Q3 + 1.5 * IQR))

        if 0 < (mask.sum() / len(df_res)) <= 0.05:
            df_res = df_res[~mask]

    return df_res
