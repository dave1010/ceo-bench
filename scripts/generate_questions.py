"""Generate CEO Bench question YAML files.

This script can produce simple placeholder questions or use the ``llm`` CLI to
create real questions with rubrics.  Topics are read from ``data/topics.yaml``.

Usage::

    python generate_questions.py [--model gpt-4.1-mini]
"""

import argparse
import subprocess
import yaml
from pathlib import Path
import re

DATA_DIR = Path("data")

TOPICS_FILE = DATA_DIR / "topics.yaml"
OUTPUT_DIR = DATA_DIR / "questions"
TEMPLATES_DIR = Path("templates")
DEFAULT_TEMPLATE = TEMPLATES_DIR / "question_gen_prompt.txt"

ID_RE = re.compile(r"^(\d+)-")


def next_id() -> int:
    max_id = 0
    for path in OUTPUT_DIR.glob("*.yaml"):
        m = ID_RE.match(path.name)
        if m:
            max_id = max(max_id, int(m.group(1)))
    return max_id + 1


def build_filename(qid: int, topic: str, subtopic: str, title: str) -> Path:
    """Return a safe path for a new question file."""
    safe_topic = topic.replace(" ", "_")
    safe_sub = subtopic.replace(" ", "_")
    safe_title = title.replace(" ", "_")
    name = f"{qid:04d}-{safe_topic}-{safe_sub}-{safe_title}.yaml"
    return OUTPUT_DIR / name


def create_question(topic: str, subtopic: str) -> dict:
    question_text = f"How would you approach the challenge of {subtopic.lower()}?"
    return {
        "topic": topic,
        "subtopic": subtopic,
        "title": subtopic,
        "question": question_text,
        "rubric": [
            {"dimension": "Clarity", "ideal": "Answer is clear and structured."},
            {"dimension": "Insight", "ideal": "Demonstrates thoughtful reasoning."},
        ],
    }


def existing_titles(topic: str, subtopic: str) -> list[str]:
    """Return a list of question titles already generated for this subtopic."""
    titles = []
    safe_topic = topic.replace(" ", "_")
    safe_sub = subtopic.replace(" ", "_")
    pattern = f"*-{safe_topic}-{safe_sub}-*.yaml"
    for path in OUTPUT_DIR.glob(pattern):
        try:
            data = yaml.safe_load(path.read_text())
        except Exception:
            continue
        if isinstance(data, dict) and data.get("title"):
            titles.append(str(data["title"]))
    return titles


def build_prompt(topic: str, subtopic: str, titles: list[str], template_file: Path) -> str:
    tmpl = template_file.read_text()
    joined = "\n".join(f"- {t}" for t in titles) if titles else "none"
    return tmpl.format(topic=topic, subtopic=subtopic, existing_titles=joined)


def call_llm(prompt: str, model: str) -> str:
    result = subprocess.run([
        "llm",
        "prompt",
        "-m",
        model,
        prompt,
    ], capture_output=True, text=True, check=True)
    return result.stdout.strip()


def extract_yaml(text: str) -> str:
    """Return YAML block from llm output."""
    if "```" in text:
        parts = text.split("```")
        if len(parts) >= 3:
            # assume yaml block is the part between first and last fences
            block = "".join(parts[1:-1]).strip()
            if block.startswith("yaml\n"):
                block = block[5:]
            return block
    return text.strip()


def create_question_llm(topic: str, subtopic: str, titles: list[str], model: str, template_file: Path) -> dict:
    prompt = build_prompt(topic, subtopic, titles, template_file)
    text = call_llm(prompt, model)
    try:
        return yaml.safe_load(extract_yaml(text))
    except yaml.YAMLError:
        print("Failed to parse YAML from llm output, falling back to placeholder question")
        return create_question(topic, subtopic)


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
