"""Generate a text prompt from a question YAML file.

Usage:
    python make_question_prompt.py path/to/question.yaml [--template prompts/question_prompt.txt]
"""

import argparse
from pathlib import Path
import yaml
from string import Template

DEFAULT_TEMPLATE = Path("prompts/question_prompt.txt")


def build_prompt(question_file: Path, template_file: Path) -> str:
    data = yaml.safe_load(question_file.read_text())
    question_text = data.get("question", "").strip()
    tmpl = Template(template_file.read_text())
    return tmpl.safe_substitute(question=question_text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Create prompt for an LLM")
    parser.add_argument("question", type=Path, help="Question YAML file")
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE, help="Prompt template")
    args = parser.parse_args()

    prompt = build_prompt(args.question, args.template)
    print(prompt)


if __name__ == "__main__":
    main()
