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
import yaml

DATA_DIR = Path("data")

RESULTS_DIR = DATA_DIR / "results"
LEADERBOARD_PATH = DATA_DIR / "leaderboard" / "leaderboard.csv"
TOPICS_FILE = DATA_DIR / "topics.yaml"


def load_results():
    records = []
    for path in RESULTS_DIR.glob("*.json"):
        with path.open() as f:
            data = json.load(f)
            records.append(data)
    return records


def load_topics():
    data = yaml.safe_load(TOPICS_FILE.read_text())
    return [t.get("name") for t in data.get("topics", [])]


def aggregate(records, topics):
    overall = defaultdict(list)
    by_topic = defaultdict(lambda: defaultdict(list))

    for rec in records:
        model = rec.get("model")
        total = rec.get("total")
        topic = rec.get("topic")
        if model is None or total is None or topic is None:
            continue
        overall[model].append(float(total))
        by_topic[model][topic].append(float(total))

    rows = []
    for model, vals in overall.items():
        row = {"model": model, "overall": round(sum(vals) / len(vals), 3), "n": len(vals)}
        for t in topics:
            tvals = by_topic[model].get(t)
            if tvals:
                row[t] = round(sum(tvals) / len(tvals), 3)
            else:
                row[t] = ""
        rows.append(row)
    return rows


def write_csv(rows, topics):
    LEADERBOARD_PATH.parent.mkdir(exist_ok=True)
    fieldnames = ["model", "overall", "n"] + topics
    with LEADERBOARD_PATH.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    records = load_results()
    topics = load_topics()
    rows = aggregate(records, topics)
    write_csv(rows, topics)
    print(f"Wrote {LEADERBOARD_PATH}")


if __name__ == "__main__":
    main()
