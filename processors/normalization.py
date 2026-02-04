from sklearn.preprocessing import MinMaxScaler, StandardScaler

def normalize(df, method="minmax"):
    num_cols = df.select_dtypes(include=["number"]).columns
    if len(num_cols) == 0:
        return df

    scaler = (
        MinMaxScaler(feature_range=(-1, 1))
        if method == "minmax"
        else StandardScaler()
    )

    df[num_cols] = scaler.fit_transform(df[num_cols])
    return df
