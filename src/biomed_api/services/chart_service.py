from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from biomed_api.models.schemas import ChartArtifact


OUTPUT_DIR = Path("output")


def _require_columns(df: pd.DataFrame, required: list[str], context: str) -> None:
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"Cannot generate {context}. Missing columns: {', '.join(missing)}")


def _safe_category_from_name(name: str) -> str:
    if name.startswith("clinical_"):
        return "clinical"
    if name.startswith("biomarker_"):
        return "biomarker"
    if name.startswith("survival_"):
        return "survival"
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


def _kaplan_like(
    df: pd.DataFrame,
    time_col: str,
    event_col: str,
    group_col: str,
) -> pd.DataFrame:
    plot_rows: list[dict[str, object]] = []
    for group_value, group_df in df.dropna(subset=[time_col]).groupby(group_col, dropna=False):
        if group_df.empty:
            continue
        work = group_df[[time_col, event_col]].copy()
        work[event_col] = work[event_col].fillna(0).astype(int)
        work = work.sort_values(time_col)
        n_at_risk = len(work)
        survival = 1.0
        plot_rows.append({"group": str(group_value), "time": 0.0, "survival": 1.0})
        for _, row in work.iterrows():
            event = int(row[event_col])
            time = float(row[time_col])
            if n_at_risk <= 0:
                break
            if event == 1:
                survival *= 1.0 - (1.0 / float(n_at_risk))
            plot_rows.append({"group": str(group_value), "time": time, "survival": survival})
            n_at_risk -= 1

    return pd.DataFrame(plot_rows)


def _write_png(fig: go.Figure, output_path: Path) -> None:
    fig.write_image(str(output_path), format="png")


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

    _require_columns(
        df, ["age_months", "stage", "risk_group", "efs_months", "event"], "clinical charts"
    )
    _require_columns(df, ["mycn_amplified"], "survival charts")

    expr_columns = [c for c in df.columns if c.startswith("expr_")]
    if not expr_columns:
        raise ValueError(
            "Cannot generate biomarker charts. No 'expr_' biomarker columns were found."
        )

    chart_defs: list[tuple[str, str, go.Figure]] = []

    chart_defs.append(
        (
            "clinical_age_distribution",
            "clinical",
            px.histogram(df, x="age_months", nbins=20, title="Age Distribution (Months)"),
        )
    )

    stage_counts = df["stage"].fillna("<missing>").value_counts().reset_index()
    stage_counts.columns = ["stage", "count"]
    chart_defs.append(
        (
            "clinical_stage_distribution",
            "clinical",
            px.bar(stage_counts, x="stage", y="count", title="Stage Distribution"),
        )
    )

    risk_counts = df["risk_group"].fillna("<missing>").value_counts().reset_index()
    risk_counts.columns = ["risk_group", "count"]
    chart_defs.append(
        (
            "clinical_risk_distribution",
            "clinical",
            px.bar(risk_counts, x="risk_group", y="count", title="Risk Group Distribution"),
        )
    )

    chart_defs.append(
        (
            "clinical_efs_by_risk",
            "clinical",
            px.box(df, x="risk_group", y="efs_months", points="all", title="EFS by Risk Group"),
        )
    )

    biomarker_melt = df[expr_columns].melt(var_name="biomarker", value_name="expression")
    chart_defs.append(
        (
            "biomarker_expression_summary",
            "biomarker",
            px.box(
                biomarker_melt,
                x="biomarker",
                y="expression",
                points=False,
                title="Biomarker Expression Summary",
            ),
        )
    )

    scatter_cols = [c for c in ("expr_mycn", "expr_alk") if c in df.columns]
    if len(scatter_cols) == 2:
        chart_defs.append(
            (
                "biomarker_mycn_vs_alk",
                "biomarker",
                px.scatter(
                    df,
                    x="expr_mycn",
                    y="expr_alk",
                    color="event",
                    title="MYCN vs ALK Expression",
                ),
            )
        )

    corr = df[expr_columns].corr(numeric_only=True)
    chart_defs.append(
        (
            "biomarker_correlation_heatmap",
            "biomarker",
            px.imshow(corr, text_auto=False, title="Biomarker Correlation Heatmap"),
        )
    )

    km_risk = _kaplan_like(df, "efs_months", "event", "risk_group")
    chart_defs.append(
        (
            "survival_km_by_risk",
            "survival",
            px.line(km_risk, x="time", y="survival", color="group", title="KM-Style Curve by Risk"),
        )
    )

    km_mycn = _kaplan_like(df, "efs_months", "event", "mycn_amplified")
    chart_defs.append(
        (
            "survival_km_by_mycn",
            "survival",
            px.line(km_mycn, x="time", y="survival", color="group", title="KM-Style Curve by MYCN"),
        )
    )

    event_rates = (
        df.groupby(["risk_group", "mycn_amplified"], dropna=False)["event"]
        .mean()
        .reset_index(name="event_rate")
    )
    event_pivot = event_rates.pivot(
        index="risk_group", columns="mycn_amplified", values="event_rate"
    )
    chart_defs.append(
        (
            "survival_event_rate_heatmap",
            "survival",
            px.imshow(event_pivot, text_auto=True, title="Event Rate Heatmap: Risk x MYCN"),
        )
    )

    corr_to_event = (
        df[expr_columns + ["event"]]
        .corr(numeric_only=True)["event"]
        .drop(labels=["event"], errors="ignore")
    )
    top_markers = corr_to_event.abs().sort_values(ascending=False).head(2).index.tolist()
    for marker in top_markers:
        split_df = df[[marker, "efs_months", "event"]].copy()
        split_df["group"] = np.where(split_df[marker] >= split_df[marker].median(), "high", "low")
        km_marker = _kaplan_like(split_df, "efs_months", "event", "group")
        safe_marker = marker.replace("expr_", "")
        chart_defs.append(
            (
                f"survival_km_median_split_{safe_marker}",
                "survival",
                px.line(
                    km_marker,
                    x="time",
                    y="survival",
                    color="group",
                    title=f"KM-Style Median Split: {marker}",
                ),
            )
        )

    for name, category, fig in chart_defs:
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