from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from csv_analyser.services.data_service import build_summary, infer_schema, load_dataset


def test_load_dataset_normalizes_columns(tmp_path: Path) -> None:
    csv_path = tmp_path / "sample.csv"
    csv_path.write_text("Order ID,Total Price\nORD001,10\n", encoding="utf-8")

    df = load_dataset(csv_path)

    assert "order_id" in df.columns
    assert "total_price" in df.columns
    assert int(df.loc[0, "total_price"]) == 10


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
            "category": ["Electronics", "Accessories"],
            "city": ["New York", "London"],
            "quantity": [10, 5],
        }
    )

    summary = build_summary(df)

    assert summary["row_count"] == 2
    assert summary["column_count"] == 3
    assert "key_distributions" in summary
