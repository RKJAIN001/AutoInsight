import pandas as pd

def get_missing_summary(df):
    """Returns a small report of which columns have missing values and their type."""
    missing = df.isnull().sum()
    missing = missing[missing > 0]

    report = []
    for col, count in missing.items():
        col_type = "numeric" if pd.api.types.is_numeric_dtype(df[col]) else "categorical"
        report.append({
            "column": col,
            "missing_count": int(count),
            "missing_pct": round(count / len(df) * 100, 1),
            "type": col_type
        })
    return report

def clean_dataset(df, numeric_strategy="mean", categorical_strategy="mode"):
    """
    Fills missing values based on column type.
    numeric_strategy: "mean" or "median"
    categorical_strategy: "mode" (most frequent value)

    Returns: (cleaned_df, log) where log describes what was changed, for transparency.
    """
    df_clean = df.copy()
    log = []

    for col in df_clean.columns:
        missing_count = df_clean[col].isnull().sum()
        if missing_count == 0:
            continue

        if pd.api.types.is_numeric_dtype(df_clean[col]):
            if numeric_strategy == "mean":
                fill_value = df_clean[col].mean()
            else:
                fill_value = df_clean[col].median()
            df_clean[col] = df_clean[col].fillna(fill_value)
            log.append(f"'{col}': filled {missing_count} missing value(s) with {numeric_strategy} ({fill_value:,.2f})")

        else:
            if df_clean[col].mode().empty:
                # Extremely rare edge case: entire column is missing, nothing to compute a mode from
                fill_value = "Unknown"
            else:
                fill_value = df_clean[col].mode()[0]
            df_clean[col] = df_clean[col].fillna(fill_value)
            log.append(f"'{col}': filled {missing_count} missing value(s) with most frequent value ('{fill_value}')")

    return df_clean, log