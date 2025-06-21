"""Generate CEO Bench question YAML files.

This script can produce simple placeholder questions or use the ``llm`` CLI to
create real questions with rubrics.  Topics are read from ``data/topics.yaml``.

Usage::

    python generate_questions.py [--model gpt-4.1-mini]
"""

import argparse
import yaml
from pathlib import Path

import sys
from pathlib import Path

if __package__ is None:
    sys.path.append(str(Path(__file__).resolve().parents[1]))
    from scripts.question_utils import (
        DATA_DIR,
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
    from .question_utils import (
        DATA_DIR,
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
        "--template", type=Path, default=DEFAULT_TEMPLATE, help="Prompt template"
    )
    args = parser.parse_args()

    if not TOPICS_FILE.exists():
        raise SystemExit(f"Missing {TOPICS_FILE}")

    OUTPUT_DIR.mkdir(exist_ok=True)

    data = yaml.safe_load(TOPICS_FILE.read_text())

    qid = next_id()
    for topic in data.get("topics", []):
        tname = topic.get("name")
        for subtopic in topic.get("subtopics", []):
            for _ in range(args.questions_per_subtopic):
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
