import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from scripts.aggregate_results import aggregate  # noqa: E402


def test_aggregate_computes_averages():
    records = [
        {"model": "A", "total": 4.0, "topic": "X"},
        {"model": "A", "total": 5.0, "topic": "Y"},
        {"model": "B", "total": 2.0, "topic": "X"},
    ]
    rows = aggregate(records, ["X", "Y"], {"A": "Model A", "B": "Model B"})
    data = {row["model"]: row for row in rows}
    assert data["A"]["overall"] == 4.5
    assert data["A"]["n"] == 2
    assert data["A"]["X"] == 4.0
    assert data["A"]["Y"] == 5.0
    assert data["B"]["overall"] == 2.0
    assert data["B"]["n"] == 1
    assert data["A"]["model_name"] == "Model A"


def test_model_name_fallback(capsys):
    records = [{"model": "X", "total": 3.0, "topic": "T"}]
    rows = aggregate(records, ["T"], {})
    captured = capsys.readouterr()
    assert rows[0]["model_name"] == "X"
    assert "Add the name to the yaml" in captured.out


def test_rows_sorted_by_model_id():
    records = [
        {"model": "B", "total": 2.0, "topic": "T"},
        {"model": "A", "total": 1.0, "topic": "T"},
    ]
    rows = aggregate(records, ["T"], {"A": "A", "B": "B"})
    assert [r["model"] for r in rows] == ["A", "B"]
