from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from csv_analyser.models.schemas import ChartArtifact


OUTPUT_DIR = Path("output")


def _has_columns(df: pd.DataFrame, required: list[str]) -> bool:
    return all(col in df.columns for col in required)


def _safe_category_from_name(name: str) -> str:
    if name.startswith("overview_"):
        return "overview"
    if name.startswith("correlation_"):
        return "correlation"
    if name.startswith("distribution_"):
        return "distribution"
    if name.startswith("category_"):
        return "category"
    if name.startswith("time_series_"):
        return "time"
    return "other"


def ensure_output_dir(output_dir: str | Path | None = None, clean: bool = False) -> Path:
    directory = Path(output_dir) if output_dir is not None else OUTPUT_DIR
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "images").mkdir(parents=True, exist_ok=True)
    if clean:
        for item in directory.rglob("*"):
            if item.name == ".gitkeep":
                continue
            if item.is_file():
                item.unlink()
    return directory


def _write_png(fig: go.Figure, output_path: Path) -> None:
    fig.write_image(str(output_path), format="png")


def _safe_col_name(col: str, max_len: int = 30) -> str:
    """Convert a column name to a filesystem-safe string."""
    safe = col.replace(" ", "_").replace("/", "_").replace("\\", "_")
    safe = "".join(c for c in safe if c.isalnum() or c == "_")
    return safe[:max_len]


def generate_standard_charts(
    df: pd.DataFrame,
    output_dir: str | Path | None = None,
    clean_output: bool = True,
    write_png: bool = True,
) -> list[ChartArtifact]:
    _ = write_png
    directory = ensure_output_dir(output_dir, clean=clean_output)
    image_directory = directory / "images"
    artifacts: list[ChartArtifact] = []

    # Identify column types
    numeric_cols = [
        c for c in df.columns
        if pd.api.types.is_numeric_dtype(df[c]) and df[c].notna().sum() > 0
    ]
    date_cols = [
        c for c in df.columns
        if pd.api.types.is_datetime64_any_dtype(df[c]) and df[c].notna().sum() > 0
    ]
    cat_cols = [
        c for c in df.columns
        if not pd.api.types.is_numeric_dtype(df[c])
        and not pd.api.types.is_datetime64_any_dtype(df[c])
        and 2 <= df[c].nunique() <= 50
    ]

    chart_defs: list[tuple[str, str, go.Figure]] = []

    # --- Overview: numeric box plots ---
    if len(numeric_cols) >= 2:
        melt = df[numeric_cols].melt(var_name="column", value_name="value")
        chart_defs.append((
            "overview_numeric_distributions",
            "overview",
            px.box(melt, x="column", y="value", title="Numeric Column Distributions"),
        ))
    elif len(numeric_cols) == 1:
        col = numeric_cols[0]
        chart_defs.append((
            f"overview_numeric_distributions",
            "overview",
            px.histogram(df, x=col, nbins=20, title=f"Distribution: {col}"),
        ))

    # --- Correlation heatmap ---
    if len(numeric_cols) >= 2:
        corr = df[numeric_cols].corr(numeric_only=True)
        chart_defs.append((
            "correlation_heatmap",
            "correlation",
            px.imshow(corr, text_auto=".2f", title="Correlation Heatmap"),
        ))

    # --- Individual distributions (top 6 numeric columns) ---
    for col in numeric_cols[:6]:
        safe_name = _safe_col_name(col)
        chart_defs.append((
            f"distribution_{safe_name}",
            "distribution",
            px.histogram(df, x=col, nbins=20, title=f"Distribution: {col}"),
        ))

    # --- Categorical bar charts (top 8, limit to top 15 values each) ---
    for col in cat_cols[:8]:
        counts = df[col].fillna("<missing>").value_counts().head(15).reset_index()
        counts.columns = [col, "count"]
        safe_name = _safe_col_name(col)
        chart_defs.append((
            f"category_{safe_name}",
            "category",
            px.bar(counts, x=col, y="count", title=f"Top Values: {col}"),
        ))

    # --- Time series (date col + numeric cols) ---
    if date_cols and numeric_cols:
        date_col = date_cols[0]
        # Generate a time series for each of the first 3 numeric columns
        for num_col in numeric_cols[:3]:
            ts_df = df[[date_col, num_col]].dropna().sort_values(date_col).copy()
            ts_df["_period"] = ts_df[date_col].dt.to_period("M").dt.to_timestamp()
            ts_agg = ts_df.groupby("_period")[num_col].sum().reset_index()
            ts_agg.columns = ["period", num_col]
            safe_name = _safe_col_name(num_col)
            chart_defs.append((
                f"time_series_{safe_name}",
                "time",
                px.line(ts_agg, x="period", y=num_col, title=f"Monthly Trend: {num_col}"),
            ))

    # --- Scatter of top 2 correlated numeric columns ---
    if len(numeric_cols) >= 2:
        corr = df[numeric_cols].corr(numeric_only=True).abs()
        best_pair: tuple[str, str] | None = None
        best_val = 0.0
        for i, c1 in enumerate(corr.columns):
            for c2 in corr.columns[i + 1:]:
                val = float(corr.loc[c1, c2])
                if val > best_val and val < 1.0:
                    best_val = val
                    best_pair = (c1, c2)
        if best_pair:
            c1, c2 = best_pair
            color_col = cat_cols[0] if cat_cols else None
            chart_defs.append((
                f"overview_scatter_{_safe_col_name(c1)}_vs_{_safe_col_name(c2)}",
                "overview",
                px.scatter(
                    df,
                    x=c1,
                    y=c2,
                    color=color_col,
                    title=f"Scatter: {c1} vs {c2}",
                ),
            ))

    for name, category, fig in chart_defs:
        try:
            png_path = image_directory / f"{name}.png"
            _write_png(fig, png_path)
            artifacts.append(
                ChartArtifact(
                    name=png_path.name,
                    category=category,
                    format="png",
                    path=str(png_path),
                )
            )
        except Exception:
            pass

    return artifacts


def list_chart_artifacts(output_dir: str | Path | None = None) -> list[ChartArtifact]:
    directory = ensure_output_dir(output_dir, clean=False)
    image_directory = directory / "images"
    artifacts: list[ChartArtifact] = []
    for path in sorted(image_directory.glob("*.png")):
        if not path.is_file() or path.name == ".gitkeep":
            continue
        artifacts.append(
            ChartArtifact(
                name=path.name,
                category=_safe_category_from_name(path.stem),
                format="png",
                path=str(path),
            )
        )
    return artifacts


def get_chart_path(name: str, output_dir: str | Path | None = None) -> Path:
    directory = ensure_output_dir(output_dir, clean=False)
    target = directory / "images" / name
    if not target.exists() or not target.is_file():
        raise FileNotFoundError(f"Chart '{name}' was not found in '{directory / 'images'}'.")
    return target
