import numpy as np

def analyze_data(df):
    num_cols = df.select_dtypes(include=[np.number]).columns
    outliers_count = 0

    for col in num_cols:
        Q1, Q3 = df[col].quantile(0.25), df[col].quantile(0.75)
        IQR = Q3 - Q1
        outliers_count += (
            (df[col] < (Q1 - 1.5 * IQR)) |
            (df[col] > (Q3 + 1.5 * IQR))
        ).sum()

    return {
        "shape": list(df.shape),
        "missing_total": int(df.isnull().sum().sum()),
        "duplicates": int(df.duplicated().sum()),
        "outliers_total": int(outliers_count)
    }
