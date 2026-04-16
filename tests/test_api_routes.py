from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from csv_analyser.api import routes
from csv_analyser.main import app


client = TestClient(app)


def _upload_seed_csv() -> None:
    csv_content = (
        "order_id,product,category,city,quantity,unit_price,total_price\n"
        "ORD001,Monitor,Electronics,New York,10,349.99,3499.90\n"
        "ORD002,Mouse,Accessories,London,5,29.99,149.95\n"
        "ORD003,Keyboard,Accessories,Paris,8,79.99,639.92\n"
    )
    response = client.post(
        "/upload/csv",
        files={"file": ("uploaded.csv", csv_content, "text/csv")},
    )
    assert response.status_code == 200


def test_health_endpoint() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_home_page_renders() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert "CSV Analyser Dashboard" in response.text


def test_upload_csv_endpoint_overwrites_dataset(tmp_path: Path, monkeypatch) -> None:
    target_path = tmp_path / "data.csv"
    monkeypatch.setattr(routes, "DATA_PATH", target_path)

    csv_content = "order_id,product,category,city,quantity,unit_price,total_price\nORD001,Monitor,Electronics,New York,10,349.99,3499.90\n"
    response = client.post(
        "/upload/csv",
        files={"file": ("uploaded.csv", csv_content, "text/csv")},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["dataset_path"].endswith("data.csv")
    assert body["row_count"] == 1
    assert target_path.exists()


def test_summary_endpoint() -> None:
    _upload_seed_csv()
    response = client.get("/summary")

    assert response.status_code == 200
    body = response.json()
    assert body["row_count"] > 0
    assert body["column_count"] > 0
    assert isinstance(body["columns"], list)


def test_execute_endpoint() -> None:
    _upload_seed_csv()
    response = client.post("/execute", json={"clean_output": True, "write_png": True})

    assert response.status_code == 200
    body = response.json()
    assert body["charts_generated"] > 0
    assert body["png_charts"] > 0
    assert body["html_charts"] == 0
    assert body["report_path"].endswith("report.md")
    assert body["insights_path"].endswith("insights.md")
    assert body["insights_html_path"].endswith("insights.html")


def test_generate_charts_and_list_and_fetch() -> None:
    _upload_seed_csv()
    response = client.post("/generate/charts", json={"clean_output": True, "write_png": True})
    assert response.status_code == 200
    payload = response.json()
    assert payload["charts_generated"] > 0
    assert all(chart["format"] == "png" for chart in payload["charts"])

    charts_response = client.get("/charts")
    assert charts_response.status_code == 200
    charts = charts_response.json()["charts"]
    assert charts

    first_chart_name = charts[0]["name"]
    chart_response = client.get(f"/charts/{first_chart_name}")
    assert chart_response.status_code == 200


def test_viewer_route_renders_plotly_viewer() -> None:
    _upload_seed_csv()

    generate_response = client.post(
        "/generate/charts",
        json={"clean_output": True, "write_png": True},
    )
    assert generate_response.status_code == 200

    charts_response = client.get("/charts")
    first_chart_name = charts_response.json()["charts"][0]["name"]

    response = client.get(f"/viewer/{first_chart_name}")
    assert response.status_code == 200
    assert "plotly-image-view" in response.text
    assert "X Close" in response.text


def test_generate_and_get_report() -> None:
    _upload_seed_csv()
    gen_response = client.post("/generate/report")
    assert gen_response.status_code == 200
    assert gen_response.json()["report_path"].endswith("report.md")

    report_response = client.get("/report")
    assert report_response.status_code == 200
    assert "Dataset Snapshot" in report_response.json()["content"]


def test_generate_and_get_insights() -> None:
    _upload_seed_csv()
    charts_response = client.post("/generate/charts", json={"clean_output": True, "write_png": True})
    assert charts_response.status_code == 200

    insights_gen_response = client.post("/generate/insights")
    assert insights_gen_response.status_code == 200
    body = insights_gen_response.json()
    assert body["insights_path"].endswith("insights.md")
    assert body["insights_html_path"].endswith("insights.html")
    assert body["files_generated"] > 0

    insights_response = client.get("/insights")
    assert insights_response.status_code == 200
    assert "Final Data Insights" in insights_response.json()["content"]


def test_generate_response_to_objectives_returns_model_used(
    tmp_path: Path, monkeypatch
) -> None:
    objectives_path = tmp_path / "OBJECTIVES.md"
    objectives_path.write_text("- 1.1 Test objective\n", encoding="utf-8")
    monkeypatch.setattr(routes, "OBJECTIVES_PATH", objectives_path)

    output_path = tmp_path / "RESPONSE_TO_OBJECTIVES.md"
    output_path.write_text("# Response to Objectives\n", encoding="utf-8")

    def _fake_generate_response_to_objectives(_artifacts):
        return output_path, output_path

    monkeypatch.setattr(routes, "generate_response_to_objectives", _fake_generate_response_to_objectives)

    response = client.post("/generate/response-to-objectives")
    assert response.status_code == 200
    body = response.json()
    assert body["path"].endswith("RESPONSE_TO_OBJECTIVES.md")
    assert body["objectives_found"] == 1
    assert body["model_used"] == routes.OBJECTIVES_MODEL
