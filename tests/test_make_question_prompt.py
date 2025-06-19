import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))
from scripts.make_question_prompt import build_prompt


def test_build_prompt_substitutes_question():
    qfile = Path('data/questions/0001-Strategic_Thinking-Market_entry_strategies-European_Expansion.yaml')
    template = Path('templates/question_prompt.txt')
    result = build_prompt(qfile, template)
    assert '{question}' not in result
    # ensure the question text from YAML appears in output
    assert 'You are the CEO' in result


def test_build_prompt_missing_file():
    with pytest.raises(FileNotFoundError):
        build_prompt(Path('data/questions/path-to-missing-file-should-error'), Path('templates/question_prompt.txt'))

