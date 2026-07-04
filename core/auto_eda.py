import pandas as pd
import plotly.express as px

def classify_columns(df):
    """
    Sorts columns into buckets based on their type and characteristics,
    so we know what kind of chart fits each one.
    """
    numeric_cols = list(df.select_dtypes(include="number").columns)
    categorical_cols = list(df.select_dtypes(include="object").columns)

    # Categorical columns with few unique values are good for bar/pie charts.
    # Ones with many unique values (like names or IDs) aren't useful to chart directly.
    chartable_categorical = [
        col for col in categorical_cols
        if df[col].nunique() <= 15 and df[col].nunique() > 1
    ]

    # Try to detect date-like columns even if pandas read them as text
    date_cols = []
    for col in df.columns:
        if "date" in col.lower() or "time" in col.lower() or "year" in col.lower():
            date_cols.append(col)

    return {
        "numeric": numeric_cols,
        "categorical": chartable_categorical,
        "date_like": date_cols
    }

def generate_auto_charts(df, chart_colors, max_charts=6):
    """
    Automatically builds a set of relevant charts based on what's in the data.
    Returns a list of (title, plotly_figure) tuples.
    """
    columns = classify_columns(df)
    charts = []

    # 1. Distribution of each numeric column (histogram)
    for col in columns["numeric"][:3]:
        fig = px.histogram(df, x=col, nbins=30, color_discrete_sequence=[chart_colors["accent"][0]])
        fig.update_layout(
            paper_bgcolor=chart_colors["paper"], plot_bgcolor=chart_colors["plot"],
            font_color=chart_colors["font"], height=320, margin=dict(t=30, b=20, l=10, r=10),
            title=f"Distribution of {col}"
        )
        fig.update_xaxes(gridcolor=chart_colors["grid"])
        fig.update_yaxes(gridcolor=chart_colors["grid"])
        charts.append((f"Distribution of {col}", fig))

    # 2. Bar chart for each categorical column (count per category)
    for col in columns["categorical"][:3]:
        counts = df[col].value_counts().reset_index()
        counts.columns = [col, "count"]
        fig = px.bar(counts, x=col, y="count", color_discrete_sequence=[chart_colors["accent"][1]])
        fig.update_layout(
            paper_bgcolor=chart_colors["paper"], plot_bgcolor=chart_colors["plot"],
            font_color=chart_colors["font"], height=320, margin=dict(t=30, b=20, l=10, r=10),
            title=f"Count by {col}"
        )
        fig.update_xaxes(gridcolor=chart_colors["grid"])
        fig.update_yaxes(gridcolor=chart_colors["grid"])
        charts.append((f"Count by {col}", fig))

    # 3. If we have both a numeric and categorical column, show a comparison
    if columns["numeric"] and columns["categorical"]:
        num_col = columns["numeric"][0]
        cat_col = columns["categorical"][0]
        grouped = df.groupby(cat_col)[num_col].mean().reset_index()
        fig = px.bar(grouped, x=cat_col, y=num_col, color_discrete_sequence=[chart_colors["accent"][2]])
        fig.update_layout(
            paper_bgcolor=chart_colors["paper"], plot_bgcolor=chart_colors["plot"],
            font_color=chart_colors["font"], height=320, margin=dict(t=30, b=20, l=10, r=10),
            title=f"Average {num_col} by {cat_col}"
        )
        fig.update_xaxes(gridcolor=chart_colors["grid"])
        fig.update_yaxes(gridcolor=chart_colors["grid"])
        charts.append((f"Average {num_col} by {cat_col}", fig))

    return charts[:max_charts]

def generate_text_insights(df):
    """
    Plain-English observations about the dataset, computed automatically.
    """
    insights = []
    columns = classify_columns(df)

    insights.append(f"This dataset has {len(df):,} rows and {len(df.columns)} columns.")

    missing = df.isnull().sum()
    missing_cols = missing[missing > 0]
    if len(missing_cols) > 0:
        insights.append(f"{len(missing_cols)} column(s) have missing values: " +
                         ", ".join(f"{c} ({v})" for c, v in missing_cols.items()))
    else:
        insights.append("No missing values detected in this dataset.")

    for col in columns["numeric"][:3]:
        insights.append(
            f"'{col}' ranges from {df[col].min():,.2f} to {df[col].max():,.2f}, "
            f"averaging {df[col].mean():,.2f}."
        )

    for col in columns["categorical"][:2]:
        top_value = df[col].value_counts().idxmax()
        top_count = df[col].value_counts().max()
        insights.append(f"The most common value in '{col}' is '{top_value}' ({top_count} occurrences).")

    return insights