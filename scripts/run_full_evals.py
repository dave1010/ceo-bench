#!/usr/bin/env python
"""Run the full CEO Bench evaluation pipeline.

This script loops over all question files and specified models, generating
answers and grading them if results are missing. After processing everything it
updates the leaderboard.
"""

import argparse
import subprocess
import sys
from pathlib import Path

DATA_DIR = Path("data")
QUESTIONS_DIR = DATA_DIR / "questions"
ANSWERS_DIR = DATA_DIR / "answers"
RESULTS_DIR = DATA_DIR / "results"
SCRIPTS_DIR = Path(__file__).resolve().parent


def run(cmd: list[str]) -> None:
    """Run a subprocess command, echoing it first."""
    print(" ".join(cmd))
    subprocess.run(cmd, check=True)


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
        help="Regenerate grading even if results already exist",
    )
    args = parser.parse_args()

    questions = sorted(QUESTIONS_DIR.glob("*.yaml"))

    for model in args.models:
        model_answer_dir = ANSWERS_DIR / model
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

            result_path = RESULTS_DIR / f"{qfile.stem}-{model}.json"
            if args.rerun_grade or not result_path.exists():
                run([
                    sys.executable,
                    str(SCRIPTS_DIR / "grade_answers.py"),
                    str(qfile),
                    str(answer_path),
                    "--model",
                    model,
                ])
            else:
                print(f"Skipping grading for {qfile.stem} ({model})")

    run([sys.executable, str(SCRIPTS_DIR / "aggregate_results.py")])


if __name__ == "__main__":
    main()
