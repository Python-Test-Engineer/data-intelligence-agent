from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from biomed_api.api import routes
from biomed_api.main import app


client = TestClient(app)


def _upload_seed_csv() -> None:
    csv_content = (
        "patient id,age months,risk group,stage,efs months,event,mycn amplified,"
        "expr_mycn,expr_alk,expr_mdm2\n"
        "p1,12,low,2,30,0,0,1.2,2.0,1.1\n"
        "p2,24,high,4,12,1,1,2.6,1.1,2.4\n"
        "p3,18,intermediate,3,18,0,0,1.7,1.4,1.8\n"
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
    assert "Biomedical FastAPI Frontend" in response.text


def test_upload_csv_endpoint_overwrites_dataset(tmp_path: Path, monkeypatch) -> None:
    target_path = tmp_path / "data.csv"
    monkeypatch.setattr(routes, "DATA_PATH", target_path)

    csv_content = "patient id,age months,risk group,stage,efs months,event,mycn amplified,expr_mycn,expr_alk\np1,12,low,2,30,0,0,1.2,2.0\n"
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
    assert "Cohort Snapshot" in report_response.json()["content"]


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
    assert "Final Biomedical Insights" in insights_response.json()["content"]
