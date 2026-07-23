import pandas as pd


def inspect_dataframe(df: pd.DataFrame, name: str):
    print("=" * 70)
    print(f"{name.upper()}")
    print("=" * 70)

    print(f"\nShape: {df.shape}")

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nData Types:")
    print(df.dtypes)

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nDuplicate Rows:")
    print(df.duplicated().sum())

    print("\nSample Data:")
    print(df.head())

    print("\nSummary:")
    print(df.describe(include="all"))