"""Aggregate grading results into leaderboard data.

Usage:
    python aggregate_results.py

This script reads JSON files from ./results and computes average scores
per model. It writes CSV output to ./leaderboard/leaderboard.csv.

Each results JSON file should have the structure:
{
    "question_id": "0001",
    "model": "gpt-3.5",
    "scores": {"Strategic Depth": 4, "Feasibility": 5},
    "total": 4.5
}
"""

import json
from pathlib import Path
from collections import defaultdict
import csv

RESULTS_DIR = Path("results")
LEADERBOARD_PATH = Path("leaderboard/leaderboard.csv")


def load_results():
    records = []
    for path in RESULTS_DIR.glob("*.json"):
        with path.open() as f:
            data = json.load(f)
            records.append(data)
    return records


def aggregate(records):
    scores = defaultdict(list)
    for rec in records:
        model = rec.get("model")
        total = rec.get("total")
        if model is None or total is None:
            continue
        scores[model].append(float(total))

    rows = []
    for model, vals in scores.items():
        avg = sum(vals) / len(vals)
        rows.append({"model": model, "avg_score": round(avg, 3), "n": len(vals)})
    return rows


def write_csv(rows):
    LEADERBOARD_PATH.parent.mkdir(exist_ok=True)
    with LEADERBOARD_PATH.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["model", "avg_score", "n"])
        writer.writeheader()
        writer.writerows(rows)


def main():
    records = load_results()
    rows = aggregate(records)
    write_csv(rows)
    print(f"Wrote {LEADERBOARD_PATH}")


if __name__ == "__main__":
    main()
