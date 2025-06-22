import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from scripts.generate_questions import build_filename  # noqa: E402
import scripts.question_utils as q_utils  # noqa: E402


def test_build_filename_structure():
    path = build_filename(
        1,
        "Strategic Thinking",
        "Market Entry",
        "Market Entry",
    )
    assert path == Path(
        "data/questions/0001-Strategic_Thinking-Market_Entry-Market_Entry.yaml"
    )


def test_create_question_contains_fields():
    q = q_utils.create_question("Topic", "Sub", "board")
    assert q["topic"] == "Topic"
    assert q["subtopic"] == "Sub"
    assert q["conflict"] == "board"
    assert isinstance(q.get("rubric"), list)


def test_create_question_llm_defaults(monkeypatch):
    def fake_call_llm(prompt: str, model: str) -> str:
        return "title: Example\nquestion: Example?\n"

    monkeypatch.setattr(q_utils, "call_llm", fake_call_llm)

    data = q_utils.create_question_llm(
        "Topic", "Subtopic", [], "model", q_utils.DEFAULT_TEMPLATE
    )
    assert data["topic"] == "Topic"
    assert data["subtopic"] == "Subtopic"
    assert "conflict" in data
