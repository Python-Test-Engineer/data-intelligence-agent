from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from biomed_api.services.data_service import build_summary, infer_schema, load_dataset


def test_load_dataset_normalizes_columns(tmp_path: Path) -> None:
    csv_path = tmp_path / "sample.csv"
    csv_path.write_text("Patient ID,Value One\nNB001,10\n", encoding="utf-8")

    df = load_dataset(csv_path)

    assert "patient_id" in df.columns
    assert "value_one" in df.columns
    assert int(df.loc[0, "value_one"]) == 10


def test_infer_schema_contains_expected_keys() -> None:
    df = pd.DataFrame({"a": [1, None], "b": ["x", "y"]})

    schema = infer_schema(df)

    assert len(schema) == 2
    assert {"name", "dtype", "missing_count", "missing_pct"}.issubset(schema[0].keys())


def test_load_dataset_missing_file_raises(tmp_path: Path) -> None:
    missing_path = tmp_path / "does_not_exist.csv"

    with pytest.raises(FileNotFoundError):
        load_dataset(missing_path)


def test_build_summary_has_profile_fields() -> None:
    df = pd.DataFrame(
        {
            "risk_group": ["low", "high"],
            "stage": ["2A", "4"],
            "event": [0, 1],
        }
    )

    summary = build_summary(df)

    assert summary["row_count"] == 2
    assert summary["column_count"] == 3
    assert "key_distributions" in summary
