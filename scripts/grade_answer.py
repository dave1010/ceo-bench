"""Grade an answer using llm and store JSON results.

Usage:
    python grade_answer.py question.yaml answer.txt \
        --model MODEL_NAME [--grading-model gpt-4.1-mini]
"""

import argparse
import json
import subprocess
from pathlib import Path
import yaml

DATA_DIR = Path("data")

from make_grading_prompt import build_prompt, DEFAULT_TEMPLATE

RESULTS_DIR = DATA_DIR / "results"


def build_schema(dimensions):
    fields = [f"{dim.lower().replace(' ', '_')} int" for dim in dimensions]
    fields.append("overall_score float")
    fields.append("comments")
    return ", ".join(fields)


def call_llm(prompt: str, model: str, schema: str) -> str:
    result = subprocess.run([
        "llm",
        "prompt",
        "-m",
        model,
        "--schema",
        schema,
        prompt,
    ], capture_output=True, text=True, check=True)
    return result.stdout.strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Grade an answer using llm")
    parser.add_argument("question", type=Path, help="Question YAML file")
    parser.add_argument("answer", type=Path, help="Answer text file")
    parser.add_argument("--model", required=True, help="Model being evaluated")
    parser.add_argument(
        "--grading-model",
        default="gpt-4.1-mini",
        help="Model used to grade the answer",
    )
    args = parser.parse_args()

    qdata = yaml.safe_load(args.question.read_text())
    dimensions = [item.get("dimension") for item in qdata.get("rubric", [])]
    topic = qdata.get("topic")
    subtopic = qdata.get("subtopic")

    prompt = build_prompt(args.question, args.answer, DEFAULT_TEMPLATE)
    schema = build_schema(dimensions)
    grading_text = call_llm(prompt, args.grading_model, schema)

    try:
        parsed = json.loads(grading_text)
    except json.JSONDecodeError:
        parsed = None

    RESULTS_DIR.mkdir(exist_ok=True)
    outfile = RESULTS_DIR / f"{args.answer.stem}-{args.model}.json"
    record = {
        "question_id": args.question.stem,
        "model": args.model,
        "topic": topic,
        "subtopic": subtopic,
        "raw": grading_text,
    }
    if parsed:
        scores = {}
        for dim in dimensions:
            key = dim.lower().replace(" ", "_")
            if key in parsed:
                scores[dim] = int(parsed[key])
        total = parsed.get("overall_score")
        if total is None and scores:
            total = sum(scores.values()) / len(scores)
        record["scores"] = scores
        if total is not None:
            record["total"] = float(total)
        if "comments" in parsed:
            record["comments"] = parsed["comments"]
    outfile.write_text(json.dumps(record, indent=2))
    print(f"Wrote {outfile}")


if __name__ == "__main__":
    main()
