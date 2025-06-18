"""Generate CEO Bench questions from topic list.

Usage:
    python generate_questions.py
"""

import yaml
from pathlib import Path

TOPICS_FILE = Path("dev/topics.yaml")
OUTPUT_DIR = Path("questions")


def main():
    if not TOPICS_FILE.exists():
        raise SystemExit(f"Missing {TOPICS_FILE}")

    data = yaml.safe_load(TOPICS_FILE.read_text())
    for topic in data.get("topics", []):
        for subtopic in topic.get("subtopics", []):
            # Placeholder logic
            print(f"Would generate questions for {topic['name']} - {subtopic}")


if __name__ == "__main__":
    main()

