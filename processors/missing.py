import numpy as np

def handle_missing(df, method="fill_mean"):
    df = df.copy()
    num_cols = df.select_dtypes(include=[np.number]).columns
    cat_cols = df.select_dtypes(exclude=[np.number]).columns

    if method == "fill_mean":
        df[num_cols] = df[num_cols].fillna(df[num_cols].mean())
    elif method == "fill_median":
        df[num_cols] = df[num_cols].fillna(df[num_cols].median())
    elif method == "drop":
        df = df.dropna()

    for col in cat_cols:
        mode = df[col].mode()
        df[col] = df[col].fillna(mode[0] if not mode.empty else "Inconnu")

    return df
