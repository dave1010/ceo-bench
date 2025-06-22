"""Generate CEO Bench question YAML files.

This script can produce simple placeholder questions or use the ``llm`` CLI to
create real questions with rubrics.  Topics are read from ``data/topics.yaml``.

Usage::

    python generate_questions.py [--model gpt-4.1-mini]
"""

import argparse
import sys
from pathlib import Path
import yaml

if __package__ is None:
    sys.path.append(str(Path(__file__).resolve().parents[1]))
    from scripts.question_utils import (  # noqa: F401
        TOPICS_FILE,
        OUTPUT_DIR,
        DEFAULT_TEMPLATE,
        next_id,
        build_filename,
        existing_titles,
        create_question,
        create_question_llm,
    )
else:
    from .question_utils import (  # noqa: F401
        TOPICS_FILE,
        OUTPUT_DIR,
        DEFAULT_TEMPLATE,
        next_id,
        build_filename,
        existing_titles,
        create_question,
        create_question_llm,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate questions")
    parser.add_argument("--model", default="gpt-4.1-mini", help="Model name")
    parser.add_argument(
        "--questions-per-subtopic",
        type=int,
        default=10,
        help="Questions to generate for each subtopic",
    )
    parser.add_argument(
        "--template",
        type=Path,
        default=DEFAULT_TEMPLATE,
        help="Prompt template",
    )
    parser.add_argument(
        "--topic",
        help="Generate questions only for this topic",
    )
    parser.add_argument(
        "--subtopic",
        help="Generate questions only for this subtopic (requires --topic)",
    )
    parser.add_argument(
        "--count",
        type=int,
        help="Generate this many questions when --subtopic is used",
    )
    args = parser.parse_args()

    if args.subtopic and not args.topic:
        parser.error("--subtopic requires --topic")

    if not TOPICS_FILE.exists():
        raise SystemExit(f"Missing {TOPICS_FILE}")

    OUTPUT_DIR.mkdir(exist_ok=True)

    data = yaml.safe_load(TOPICS_FILE.read_text())

    qid = next_id()
    for topic in data.get("topics", []):
        tname = topic.get("name")
        if args.topic and tname != args.topic:
            continue
        for subtopic in topic.get("subtopics", []):
            if args.subtopic and subtopic != args.subtopic:
                continue
            count = args.count or args.questions_per_subtopic
            for _ in range(count):
                titles = existing_titles(tname, subtopic)
                qdata = create_question_llm(
                    tname, subtopic, titles, args.model, args.template
                )
                outfile = build_filename(
                    qid,
                    qdata.get("topic", tname),
                    qdata.get("subtopic", subtopic),
                    qdata.get("title", str(qid)),
                )
                outfile.write_text(yaml.safe_dump(qdata, sort_keys=False))
                print(f"Wrote {outfile}")
                qid += 1


if __name__ == "__main__":
    main()
