from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from csv_analyser.models.schemas import ChartArtifact
from csv_analyser.services.insight_service import generate_insights_bundle, read_final_insights


def _build_df() -> pd.DataFrame:
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


def test_generate_insights_bundle_writes_markdown_and_html(tmp_path: Path) -> None:
    df = _build_df()
    artifacts = [
        ChartArtifact(
            name="correlation_heatmap.png",
            category="correlation",
            format="png",
            path=str(tmp_path / "images" / "correlation_heatmap.png"),
        ),
        ChartArtifact(
            name="category_distribution.png",
            category="category",
            format="png",
            path=str(tmp_path / "images" / "category_distribution.png"),
        ),
    ]

    insights_md, insights_html, section_paths = generate_insights_bundle(
        df, artifacts, insights_dir=tmp_path / "insights"
    )

    assert insights_md.exists()
    assert insights_html.exists()
    assert len(section_paths) == 2
    for section_path in section_paths:
        content = section_path.read_text(encoding="utf-8")
        assert "## Data Insight" in content
        assert "## Analysis Insight" in content
        assert "![" in content


def test_read_final_insights_returns_path_and_content(tmp_path: Path) -> None:
    insights_path = tmp_path / "insights.md"
    insights_path.write_text("# Final Data Insights\n", encoding="utf-8")

    path, content = read_final_insights(insights_path=insights_path)

    assert path == insights_path
    assert "Final Data Insights" in content


def test_generate_insights_uses_llm_when_configured(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from csv_analyser.services import insight_service

    _LLM_JSON = (
        '{"data_insight":"LLM data insight",'
        '"analysis_insight":"LLM analysis insight",'
        '"caveat":"LLM caveat"}'
    )

    class _Stream:
        def __enter__(self) -> "_Stream":
            return self

        def __exit__(self, *_: object) -> None:
            pass

        @property
        def text_stream(self):
            return iter([_LLM_JSON])

    class _Messages:
        @staticmethod
        def stream(**_: object) -> _Stream:
            return _Stream()

    class _Client:
        def __init__(self, **_: object) -> None:
            self.messages = _Messages()

    image_dir = tmp_path / "images"
    image_dir.mkdir(parents=True, exist_ok=True)
    image_path = image_dir / "overview_distribution.png"
    image_path.write_bytes(b"\x89PNG\r\n\x1a\nfake")

    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
    monkeypatch.setattr(insight_service.anthropic, "Anthropic", _Client)

    df = _build_df()
    artifacts = [
        ChartArtifact(
            name=image_path.name,
            category="overview",
            format="png",
            path=str(image_path),
        )
    ]

    insights_md, _, _ = generate_insights_bundle(df, artifacts, insights_dir=tmp_path / "insights")
    content = insights_md.read_text(encoding="utf-8")

    assert "LLM data insight" in content
    assert "LLM analysis insight" in content
    assert "LLM caveat" in content
