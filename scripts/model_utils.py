from urllib.parse import quote, unquote


def encode_model_name(model: str) -> str:
    """Return a filesystem-safe version of the model name."""
    return quote(model, safe="")


def decode_model_name(name: str) -> str:
    """Reverse ``encode_model_name``."""
    return unquote(name)
