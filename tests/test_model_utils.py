import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from scripts.model_utils import (  # noqa: E402
    encode_model_name,
    decode_model_name,
)


def test_round_trip():
    original = "groq/llama3-8b-8192"
    encoded = encode_model_name(original)
    assert "/" not in encoded
    assert decode_model_name(encoded) == original
