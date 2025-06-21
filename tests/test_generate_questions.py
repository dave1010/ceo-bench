import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from scripts.generate_questions import build_filename, create_question  # noqa: E402


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
    q = create_question("Topic", "Sub")
    assert q["topic"] == "Topic"
    assert q["subtopic"] == "Sub"
    assert isinstance(q.get("rubric"), list)
