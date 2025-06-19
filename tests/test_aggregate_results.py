import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from scripts.aggregate_results import aggregate


def test_aggregate_computes_averages():
    records = [
        {"model": "A", "total": 4.0},
        {"model": "A", "total": 5.0},
        {"model": "B", "total": 2.0},
    ]
    rows = aggregate(records)
    data = {row["model"]: row for row in rows}
    assert data["A"]["avg_score"] == 4.5
    assert data["A"]["n"] == 2
    assert data["B"]["avg_score"] == 2.0
    assert data["B"]["n"] == 1
