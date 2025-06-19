"""Generate answers from a question YAML using the llm CLI.

Usage:
    python generate_answers.py question.yaml --model gpt-4.1-mini

The script uses make_question_prompt.py to build a prompt and then calls
`llm` to get the model's answer. The result is saved under
`answers/<model>/<question_id>.txt`.
"""

import argparse
import subprocess
from pathlib import Path

DATA_DIR = Path("data")

from make_question_prompt import build_prompt, DEFAULT_TEMPLATE

ANSWERS_DIR = DATA_DIR / "answers"


def call_llm(prompt: str, model: str) -> str:
    result = subprocess.run(
        [
            "llm",
            "prompt",
            "-m",
            model,
            prompt,
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate an answer using llm")
    parser.add_argument("question", type=Path, help="Question YAML file")
    parser.add_argument("--model", default="gpt-4.1-mini", help="Model name")
    args = parser.parse_args()

    prompt = build_prompt(args.question, DEFAULT_TEMPLATE)
    response = call_llm(prompt, args.model)

    model_dir = ANSWERS_DIR / args.model
    model_dir.mkdir(parents=True, exist_ok=True)
    outfile = model_dir / (args.question.stem + ".txt")
    outfile.write_text(response)
    print(f"Wrote {outfile}")


if __name__ == "__main__":
    main()
