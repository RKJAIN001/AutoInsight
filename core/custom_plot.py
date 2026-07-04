import plotly.express as px
import pandas as pd

PLOT_TYPES = ["Bar", "Line", "Scatter", "Histogram", "Box", "Pie"]

def build_custom_plot(df, plot_type, x_col=None, y_col=None, color_col=None, chart_colors=None):
    """
    Builds a Plotly figure based on user-selected plot type and columns.
    x_col/y_col/color_col may be None depending on what the plot type needs.
    Returns (figure, error_message). error_message is None on success.
    """
    accent_seq = chart_colors["accent"] if chart_colors else None

    try:
        if plot_type == "Bar":
            if not x_col or not y_col:
                return None, "Bar chart needs both an X and Y column."
            fig = px.bar(df, x=x_col, y=y_col, color=color_col, color_discrete_sequence=accent_seq)

        elif plot_type == "Line":
            if not x_col or not y_col:
                return None, "Line chart needs both an X and Y column."
            fig = px.line(df, x=x_col, y=y_col, color=color_col, color_discrete_sequence=accent_seq)

        elif plot_type == "Scatter":
            if not x_col or not y_col:
                return None, "Scatter plot needs both an X and Y column."
            fig = px.scatter(df, x=x_col, y=y_col, color=color_col, color_discrete_sequence=accent_seq)

        elif plot_type == "Histogram":
            if not x_col:
                return None, "Histogram needs an X column."
            fig = px.histogram(df, x=x_col, color=color_col, color_discrete_sequence=accent_seq)

        elif plot_type == "Box":
            if not y_col:
                return None, "Box plot needs a Y column (numeric)."
            fig = px.box(df, x=x_col, y=y_col, color=color_col, color_discrete_sequence=accent_seq)

        elif plot_type == "Pie":
            if not x_col:
                return None, "Pie chart needs a column to break down by."
            counts = df[x_col].value_counts().reset_index()
            counts.columns = [x_col, "count"]
            fig = px.pie(counts, names=x_col, values="count", color_discrete_sequence=accent_seq)

        else:
            return None, f"Unknown plot type: {plot_type}"

        if chart_colors:
            fig.update_layout(
                paper_bgcolor=chart_colors["paper"],
                plot_bgcolor=chart_colors["plot"],
                font_color=chart_colors["font"],
                height=420,
                margin=dict(t=30, b=20, l=10, r=10),
            )
            fig.update_xaxes(gridcolor=chart_colors["grid"])
            fig.update_yaxes(gridcolor=chart_colors["grid"])

        return fig, None

    except Exception as e:
        return None, f"Could not build this chart: {str(e)}"