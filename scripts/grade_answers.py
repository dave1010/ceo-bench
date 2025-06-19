"""Grade an answer using llm and store JSON results.

Usage:
    python grade_answers.py question.yaml answer.txt --model gpt-4.1-mini
"""

import argparse
import json
import subprocess
from pathlib import Path

from make_grading_prompt import build_prompt, DEFAULT_TEMPLATE

RESULTS_DIR = Path("results")


def call_llm(prompt: str, model: str) -> str:
    result = subprocess.run([
        "llm",
        "prompt",
        "-m",
        model,
        prompt,
    ], capture_output=True, text=True, check=True)
    return result.stdout.strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Grade an answer using llm")
    parser.add_argument("question", type=Path, help="Question YAML file")
    parser.add_argument("answer", type=Path, help="Answer text file")
    parser.add_argument("--model", default="gpt-4.1-mini", help="Model name")
    args = parser.parse_args()

    prompt = build_prompt(args.question, args.answer, DEFAULT_TEMPLATE)
    grading_text = call_llm(prompt, args.model)

    RESULTS_DIR.mkdir(exist_ok=True)
    outfile = RESULTS_DIR / f"{args.answer.stem}-{args.model}.json"
    record = {
        "question_id": args.question.stem,
        "model": args.model,
        "raw": grading_text,
    }
    outfile.write_text(json.dumps(record, indent=2))
    print(f"Wrote {outfile}")


if __name__ == "__main__":
    main()
