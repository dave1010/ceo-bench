"""Aggregate grading results into leaderboard data.

Usage:
    python aggregate_results.py

This script reads JSON grading files from ./graded_answers and computes
average scores per model. It writes CSV output to
./leaderboard/leaderboard.csv.

Each grading JSON file should have the structure:
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

GRADED_DIR = DATA_DIR / "graded_answers"
LEADERBOARD_PATH = DATA_DIR / "leaderboard" / "leaderboard.csv"
TOPICS_FILE = DATA_DIR / "topics.yaml"
MODEL_NAMES_FILE = DATA_DIR / "model_names.yaml"


def load_graded_answers():
    records = []
    for model_dir in GRADED_DIR.iterdir():
        if not model_dir.is_dir():
            continue
        for path in model_dir.glob("*.json"):
            with path.open() as f:
                data = json.load(f)
                records.append(data)
    return records


def load_topics():
    data = yaml.safe_load(TOPICS_FILE.read_text())
    return [t.get("name") for t in data.get("topics", [])]


def load_model_names():
    if MODEL_NAMES_FILE.exists():
        data = yaml.safe_load(MODEL_NAMES_FILE.read_text())
        if isinstance(data, dict):
            return data.get("model_names", {})
    return {}


def aggregate(records, topics, model_names=None):
    if model_names is None:
        model_names = {}
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
    for model in sorted(overall):
        vals = overall[model]
        if model not in model_names:
            print(
                f"Notice: model name for '{model}' not found in {MODEL_NAMES_FILE}. "
                "Using model id. Add the name to the yaml file and run aggregate_results.py again."
            )
        row = {
            "model": model,
            "model_name": model_names.get(model, model),
            "overall": round(sum(vals) / len(vals), 3),
            "n": len(vals),
        }
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
    fieldnames = ["model", "model_name", "overall", "n"] + topics
    with LEADERBOARD_PATH.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    records = load_graded_answers()
    topics = load_topics()
    model_names = load_model_names()
    rows = aggregate(records, topics, model_names)
    write_csv(rows, topics)
    print(f"Wrote {LEADERBOARD_PATH}")


if __name__ == "__main__":
    main()
