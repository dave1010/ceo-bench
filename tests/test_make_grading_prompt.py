import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from scripts.make_grading_prompt import load_rubric, build_prompt, DEFAULT_TEMPLATE


def test_load_rubric_formats_lines():
    data = {
        "rubric": [
            {"dimension": "Clarity", "ideal": "clear"},
            {"dimension": "Insight", "ideal": "deep"},
        ]
    }
    text = load_rubric(data)
    assert "- Clarity: clear" in text
    assert "- Insight: deep" in text


def test_build_prompt_replaces_placeholders():
    qfile = Path('data/questions/0001-Strategic_Thinking-Market_entry_strategies-European_Expansion.yaml')
    afile = Path('data/answers/gpt-4.1-nano/0001-Strategic_Thinking-Market_entry_strategies-European_Expansion.txt')
    prompt = build_prompt(qfile, afile, DEFAULT_TEMPLATE)
    assert '{question}' not in prompt
    assert '{answer}' not in prompt
    assert '{rubric}' not in prompt
