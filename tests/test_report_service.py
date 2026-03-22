from __future__ import annotations

from pathlib import Path

from biomed_api.services.chart_service import generate_standard_charts
from biomed_api.services.data_service import load_dataset
from biomed_api.services.report_service import generate_report, read_report


def test_generate_report_writes_required_sections(tmp_path: Path) -> None:
    df = load_dataset("data/data.csv")
    charts = generate_standard_charts(df, output_dir=tmp_path, clean_output=True, write_png=False)

    report_path = tmp_path / "report.md"
    written = generate_report(df, charts, report_path=report_path)

    assert written.exists()
    content = written.read_text(encoding="utf-8")
    assert "## Cohort Snapshot" in content
    assert "## Outcome Stratification" in content
    assert "## Top Biomarker-EFS Associations" in content
    assert "## Chart Index" in content
    assert "## Caveats" in content


def test_read_report_returns_path_and_content(tmp_path: Path) -> None:
    report_path = tmp_path / "report.md"
    report_path.write_text("# test\n", encoding="utf-8")

    path, content = read_report(report_path=report_path)

    assert path == report_path
    assert "# test" in content
