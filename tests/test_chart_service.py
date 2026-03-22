from __future__ import annotations

from pathlib import Path

from biomed_api.services.chart_service import generate_standard_charts, list_chart_artifacts
from biomed_api.services.data_service import load_dataset


def test_generate_standard_charts_creates_artifacts(tmp_path: Path) -> None:
    df = load_dataset("data/data.csv")

    artifacts = generate_standard_charts(
        df, output_dir=tmp_path, clean_output=True, write_png=True
    )

    assert artifacts
    assert all(Path(a.path).exists() for a in artifacts)
    assert all(a.format == "png" for a in artifacts)
    assert all(Path(a.path).parent.name == "images" for a in artifacts)


def test_chart_artifacts_have_required_categories(tmp_path: Path) -> None:
    df = load_dataset("data/data.csv")
    generate_standard_charts(df, output_dir=tmp_path, clean_output=True, write_png=True)

    listed = list_chart_artifacts(output_dir=tmp_path)
    categories = {item.category for item in listed}

    assert {"clinical", "biomarker", "survival"}.issubset(categories)
    assert len(listed) >= 10
