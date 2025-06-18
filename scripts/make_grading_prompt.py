"""Generate a grading prompt from a question YAML file and an answer text file.

Usage:
    python make_grading_prompt.py question.yaml answer.txt [--template prompts/grading_prompt.txt]
"""

import argparse
from pathlib import Path
import yaml
from string import Template

DEFAULT_TEMPLATE = Path("prompts/grading_prompt.txt")


def load_rubric(data: dict) -> str:
    rubric_lines = []
    for item in data.get("rubric", []):
        dim = item.get("dimension")
        ideal = item.get("ideal")
        rubric_lines.append(f"{dim}: {ideal}")
    return "\n".join(f"- {line}" for line in rubric_lines)


def build_prompt(question_file: Path, answer_file: Path, template_file: Path) -> str:
    qdata = yaml.safe_load(question_file.read_text())
    question_text = qdata.get("question", "").strip()
    rubric_text = load_rubric(qdata)

    answer_text = answer_file.read_text().strip()

    tmpl = Template(template_file.read_text())
    return tmpl.safe_substitute(question=question_text, answer=answer_text, rubric=rubric_text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Create grading prompt for an LLM")
    parser.add_argument("question", type=Path, help="Question YAML file")
    parser.add_argument("answer", type=Path, help="Answer text file")
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE, help="Prompt template")
    args = parser.parse_args()

    prompt = build_prompt(args.question, args.answer, args.template)
    print(prompt)


if __name__ == "__main__":
    main()
