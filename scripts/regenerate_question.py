"""Regenerate a single question YAML file using the llm CLI.

Usage:
    python regenerate_question.py <id> [--model gpt-4.1-mini]
"""

import argparse
import sys
from pathlib import Path
import yaml

if __package__ is None:
    sys.path.append(str(Path(__file__).resolve().parents[1]))
    from scripts.question_utils import (
        OUTPUT_DIR,
        DEFAULT_TEMPLATE,
        existing_titles,
        create_question_llm,
        build_filename,
    )
else:
    from .question_utils import (
        OUTPUT_DIR,
        DEFAULT_TEMPLATE,
        existing_titles,
        create_question_llm,
        build_filename,
    )


def find_question_file(qid: int) -> Path:
    matches = list(OUTPUT_DIR.glob(f"{qid:04d}-*.yaml"))
    if not matches:
        raise FileNotFoundError(f"No question file found for id {qid}")
    return matches[0]


def main() -> None:
    parser = argparse.ArgumentParser(description="Regenerate a question")
    parser.add_argument("id", type=int, help="Question ID")
    parser.add_argument("--model", default="gpt-4.1-mini", help="Model name")
    parser.add_argument(
        "--template",
        type=Path,
        default=DEFAULT_TEMPLATE,
        help="Prompt template",
    )
    args = parser.parse_args()

    qfile = find_question_file(args.id)
    data = yaml.safe_load(qfile.read_text())
    topic = data.get("topic")
    subtopic = data.get("subtopic")

    titles = existing_titles(topic, subtopic)
    if data.get("title") in titles:
        titles.remove(data.get("title"))

    new_data = create_question_llm(
        topic,
        subtopic,
        titles,
        args.model,
        args.template,
    )

    outfile = build_filename(
        args.id,
        new_data.get("topic", topic),
        new_data.get("subtopic", subtopic),
        new_data.get("title", data.get("title", str(args.id))),
    )

    if outfile != qfile and qfile.exists():
        qfile.unlink()

    outfile.write_text(yaml.safe_dump(new_data, sort_keys=False))
    print(f"Wrote {outfile}")


if __name__ == "__main__":
    main()
