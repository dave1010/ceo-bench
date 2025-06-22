#!/usr/bin/env python
"""Run the full CEO Bench evaluation pipeline.

This script loops over all question files and specified models, generating
answers and grading them if graded outputs are missing. After processing
everything it updates the leaderboard.
"""

import argparse
import subprocess
import sys
from pathlib import Path
import random

from model_utils import encode_model_name

DATA_DIR = Path("data")
QUESTIONS_DIR = DATA_DIR / "questions"
ANSWERS_DIR = DATA_DIR / "answers"
GRADED_DIR = DATA_DIR / "graded_answers"
SCRIPTS_DIR = Path(__file__).resolve().parent


def run(cmd: list[str]) -> None:
    """Run a subprocess command, echoing it first."""
    print(" ".join(cmd))
    subprocess.run(cmd, check=True)


def select_questions(questions: list[Path], ratio: float) -> list[Path]:
    """Return a sampled list of question files."""
    if ratio <= 0 or ratio > 1:
        raise ValueError("sample must be between 0 and 1")
    if ratio == 1:
        return questions
    k = max(1, int(len(questions) * ratio))
    return sorted(random.sample(questions, k))


def main() -> None:
    parser = argparse.ArgumentParser(description="Run full evaluations")
    parser.add_argument(
        "--models", nargs="+", required=True, help="Model names to evaluate"
    )
    parser.add_argument(
        "--rerun-answer",
        action="store_true",
        help="Regenerate answers even if they already exist",
    )
    parser.add_argument(
        "--rerun-grade",
        action="store_true",
        help="Regenerate grading even if graded answers already exist",
    )
    parser.add_argument(
        "--grading-model",
        default="gpt-4.1-mini",
        help="Model used for grading",
    )
    parser.add_argument(
        "--sample",
        type=float,
        default=1.0,
        help="Fraction of questions to run (0-1)",
    )
    args = parser.parse_args()

    questions = select_questions(
        sorted(QUESTIONS_DIR.glob("*.yaml")), args.sample
    )

    for model in args.models:
        safe_model = encode_model_name(model)
        model_answer_dir = ANSWERS_DIR / safe_model
        model_answer_dir.mkdir(parents=True, exist_ok=True)
        for qfile in questions:
            answer_path = model_answer_dir / f"{qfile.stem}.txt"
            if args.rerun_answer or not answer_path.exists():
                run([
                    sys.executable,
                    str(SCRIPTS_DIR / "generate_answers.py"),
                    str(qfile),
                    "--model",
                    model,
                ])
            else:
                print(f"Skipping answer for {qfile.stem} ({model})")

            result_path = GRADED_DIR / safe_model / f"{qfile.stem}.json"
            if args.rerun_grade or not result_path.exists():
                run([
                    sys.executable,
                    str(SCRIPTS_DIR / "grade_answer.py"),
                    str(qfile),
                    str(answer_path),
                    "--model",
                    model,
                    "--grading-model",
                    args.grading_model,
                ])
            else:
                print(f"Skipping grading for {qfile.stem} ({model})")

    run([sys.executable, str(SCRIPTS_DIR / "aggregate_results.py")])


if __name__ == "__main__":
    main()
