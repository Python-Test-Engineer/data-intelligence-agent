from __future__ import annotations

from pathlib import Path

import pandas as pd

from csv_analyser.services.chart_service import generate_standard_charts
from csv_analyser.services.report_service import generate_report, read_report


def _build_report_df() -> pd.DataFrame:
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


def test_generate_report_writes_required_sections(tmp_path: Path) -> None:
    df = _build_report_df()
    charts = generate_standard_charts(df, output_dir=tmp_path, clean_output=True, write_png=False)

    report_path = tmp_path / "report.md"
    written = generate_report(df, charts, report_path=report_path)

    assert written.exists()
    content = written.read_text(encoding="utf-8")
    assert "## Dataset Snapshot" in content
    assert "## Numeric Summary" in content
    assert "## Top Correlations" in content
    assert "## Chart Index" in content
    assert "## Caveats" in content


def test_read_report_returns_path_and_content(tmp_path: Path) -> None:
    report_path = tmp_path / "report.md"
    report_path.write_text("# test\n", encoding="utf-8")

    path, content = read_report(report_path=report_path)

    assert path == report_path
    assert "# test" in content
