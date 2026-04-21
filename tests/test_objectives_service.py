"""Tests for objectives_service pure functions."""
from __future__ import annotations

from pathlib import Path

import pytest

from csv_analyser.services.objectives_service import count_objectives
from csv_analyser.utils.html import render_markdown_to_html


def test_count_objectives_bullet_list() -> None:
    text = "- Find top products\n- Identify trends\n- Check quality"
    assert count_objectives(text) == 3


def test_count_objectives_numbered_list_dot() -> None:
    text = "1. Find top products\n2. Identify trends\n3. Check quality"
    assert count_objectives(text) == 3


def test_count_objectives_numbered_list_colon() -> None:
    text = "1: Objective A\n2: Objective B"
    assert count_objectives(text) == 2


def test_count_objectives_star_bullets() -> None:
    text = "* Goal one\n* Goal two"
    assert count_objectives(text) == 2


def test_count_objectives_free_form_prose() -> None:
    text = "Analyse sales by region.\n\nIdentify top customers.\n\nCheck monthly trends."
    assert count_objectives(text) == 3


def test_count_objectives_empty() -> None:
    assert count_objectives("") == 0


def test_generate_response_to_objectives_sends_authorization_header(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from csv_analyser.services import objectives_service

    objectives_path = tmp_path / "OBJECTIVES.md"
    objectives_path.write_text("- Check totals\n", encoding="utf-8")
    response_path = tmp_path / "RESPONSE_TO_OBJECTIVES.md"

    captured: dict[str, object] = {}

    class _Response:
        status_code = 200
        is_success = True

        @staticmethod
        def json() -> dict[str, object]:
            return {"content": [{"type": "text", "text": "## TL;DR\n- done"}]}

    def _fake_post(url: str, *, json: dict[str, object], headers: dict[str, str], timeout: float):
        captured["url"] = url
        captured["headers"] = headers
        captured["json"] = json
        captured["timeout"] = timeout
        return _Response()

    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
    monkeypatch.setattr(objectives_service.httpx, "post", _fake_post)

    out_path, html_path = objectives_service.generate_response_to_objectives(
        [],
        objectives_path=objectives_path,
        response_path=response_path,
    )

    assert out_path.exists()
    assert html_path.exists()
    assert str(captured["url"]).endswith("/v1/messages")
    headers = captured["headers"]
    assert isinstance(headers, dict)
    assert headers["Authorization"] == "Bearer test-key"
    assert headers["anthropic-version"] == "2023-06-01"
    payload = captured["json"]
    assert isinstance(payload, dict)
    assert payload["messages"][0]["role"] == "user"


def test_render_headings() -> None:
    html = render_markdown_to_html("# H1\n## H2\n### H3")
    assert "<h1>" in html
    assert "<h2>" in html
    assert "<h3>" in html


def test_render_bullet_list() -> None:
    html = render_markdown_to_html("- item one\n- item two")
    assert "<ul>" in html
    assert "<li>" in html
    assert "item one" in html


def test_render_bold_inline() -> None:
    html = render_markdown_to_html("This is **important**.")
    assert "<strong>important</strong>" in html


def test_render_italic_inline() -> None:
    html = render_markdown_to_html("This is *italic*.")
    assert "<em>italic</em>" in html


def test_render_code_inline() -> None:
    html = render_markdown_to_html("Use `SELECT *` here.")
    assert "<code>SELECT *</code>" in html


def test_render_table() -> None:
    md = "| Name | Value |\n|---|---|\n| Alice | 42 |\n| Bob | 7 |"
    html = render_markdown_to_html(md)
    assert "<table>" in html
    assert "<thead>" in html
    assert "<tbody>" in html
    assert "<th>" in html
    assert "<td>" in html
    assert "Alice" in html
    assert "42" in html


def test_render_hr() -> None:
    html = render_markdown_to_html("Above\n\n---\n\nBelow")
    assert "<hr />" in html


def test_render_image() -> None:
    html = render_markdown_to_html("![alt text](../images/foo.png)")
    assert "<img" in html
    assert "foo.png" in html


def test_render_escaped_html_in_text() -> None:
    html = render_markdown_to_html("Score > 50 & ready")
    assert "<script" not in html
    assert "&amp;" in html or "&gt;" in html or "Score" in html
