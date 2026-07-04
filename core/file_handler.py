import pandas as pd

def load_dataset(uploaded_file):
    """
    Reads an uploaded file (CSV or Excel) into a pandas DataFrame.
    CSVs can be saved in different text encodings (UTF-8, Latin-1, Windows-1252, etc.)
    depending on what tool exported them - we try the common ones in order,
    since a wrong guess raises UnicodeDecodeError rather than silently succeeding.
    """
    filename = uploaded_file.name.lower()

    if filename.endswith(".csv"):
        encodings_to_try = ["utf-8", "latin-1", "cp1252", "iso-8859-1"]
        last_error = None

        for encoding in encodings_to_try:
            try:
                uploaded_file.seek(0)  # reset file pointer before each attempt
                df = pd.read_csv(uploaded_file, encoding=encoding)
                return df
            except (UnicodeDecodeError, UnicodeError) as e:
                last_error = e
                continue

        raise ValueError(
            f"Could not read this CSV with any common encoding "
            f"(tried {', '.join(encodings_to_try)}). Original error: {last_error}"
        )

    elif filename.endswith((".xlsx", ".xls")):
        df = pd.read_excel(uploaded_file)
    else:
        raise ValueError(f"Unsupported file type: {filename}")

    return df

def get_dataset_summary(df):
    """
    Basic profile of the dataset: shape, column names/types, missing values.
    """
    summary = {
        "num_rows": len(df),
        "num_columns": len(df.columns),
        "columns": list(df.columns),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "missing_values": df.isnull().sum().to_dict(),
        "numeric_columns": list(df.select_dtypes(include="number").columns),
        "categorical_columns": list(df.select_dtypes(include="object").columns),
    }
    return summary