from __future__ import annotations

from pathlib import Path

import pandas as pd

from csv_analyser.services.chart_service import generate_standard_charts, list_chart_artifacts


def _build_chart_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "product": ["Monitor", "Mouse", "Keyboard", "Laptop", "Headset"],
            "category": ["Electronics", "Accessories", "Accessories", "Electronics", "Accessories"],
            "city": ["New York", "London", "Paris", "New York", "London"],
            "quantity": [10, 5, 8, 2, 6],
            "unit_price": [349.99, 29.99, 79.99, 999.99, 59.99],
            "total_price": [3499.90, 149.95, 639.92, 1999.98, 359.94],
            "revenue": [3499.90, 149.95, 639.92, 1999.98, 359.94],
            "discount": [0.1, 0.0, 0.05, 0.15, 0.0],
            "profit": [700.0, 45.0, 128.0, 400.0, 72.0],
        }
    )


def test_generate_standard_charts_creates_artifacts(tmp_path: Path) -> None:
    df = _build_chart_df()

    artifacts = generate_standard_charts(
        df, output_dir=tmp_path, clean_output=True, write_png=True
    )

    assert artifacts
    assert all(Path(a.path).exists() for a in artifacts)
    assert all(a.format == "png" for a in artifacts)
    assert all(Path(a.path).parent.name == "images" for a in artifacts)


def test_chart_artifacts_have_required_categories(tmp_path: Path) -> None:
    df = _build_chart_df()
    generate_standard_charts(df, output_dir=tmp_path, clean_output=True, write_png=True)

    listed = list_chart_artifacts(output_dir=tmp_path)
    categories = {item.category for item in listed}

    assert {"overview", "correlation", "distribution", "category"}.issubset(categories)
    assert len(listed) >= 8
