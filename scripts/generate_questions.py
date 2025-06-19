"""Generate CEO Bench question YAML files from topics list.

This offline version creates placeholder questions for development.

Usage:
    python generate_questions.py
"""

import yaml
from pathlib import Path
import re

DATA_DIR = Path("data")

TOPICS_FILE = Path("dev/topics.yaml")
OUTPUT_DIR = DATA_DIR / "questions"

ID_RE = re.compile(r"^(\d+)-")


def next_id() -> int:
    max_id = 0
    for path in OUTPUT_DIR.glob("*.yaml"):
        m = ID_RE.match(path.name)
        if m:
            max_id = max(max_id, int(m.group(1)))
    return max_id + 1


def build_filename(qid: int, topic: str, subtopic: str) -> Path:
    safe_topic = topic.replace(" ", "_")
    safe_sub = subtopic.replace(" ", "_")
    title = subtopic.replace(" ", "_")
    name = f"{qid:04d}-{safe_topic}-{safe_sub}-{title}.yaml"
    return OUTPUT_DIR / name


def create_question(topic: str, subtopic: str) -> dict:
    question_text = f"How would you approach the challenge of {subtopic.lower()}?"
    return {
        "topic": topic,
        "subtopic": subtopic,
        "title": subtopic,
        "question": question_text,
        "rubric": [
            {"dimension": "Clarity", "ideal": "Answer is clear and structured."},
            {"dimension": "Insight", "ideal": "Demonstrates thoughtful reasoning."},
        ],
    }


def main():
    if not TOPICS_FILE.exists():
        raise SystemExit(f"Missing {TOPICS_FILE}")

    OUTPUT_DIR.mkdir(exist_ok=True)

    data = yaml.safe_load(TOPICS_FILE.read_text())
    qid = next_id()
    for topic in data.get("topics", []):
        for subtopic in topic.get("subtopics", []):
            outfile = build_filename(qid, topic["name"], subtopic)
            if outfile.exists():
                qid += 1
                continue
            qdata = create_question(topic["name"], subtopic)
            outfile.write_text(yaml.safe_dump(qdata, sort_keys=False))
            print(f"Wrote {outfile}")
            qid += 1


if __name__ == "__main__":
    main()
