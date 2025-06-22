import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))
sys.path.append(str(Path(__file__).resolve().parents[1] / "scripts"))
from scripts import run_full_evals  # noqa: E402


def test_select_questions_sampling(tmp_path):
    files = [tmp_path / f"{i:04d}.yaml" for i in range(10)]
    for f in files:
        f.touch()
    subset = run_full_evals.select_questions(files, 0.3)
    assert len(subset) == max(1, int(len(files) * 0.3))
    assert all(s in files for s in subset)


def test_select_questions_all(tmp_path):
    files = [tmp_path / f"{i:04d}.yaml" for i in range(5)]
    for f in files:
        f.touch()
    result = run_full_evals.select_questions(files, 1)
    assert result == sorted(files)


def test_select_questions_invalid():
    with pytest.raises(ValueError):
        run_full_evals.select_questions([], 0)
