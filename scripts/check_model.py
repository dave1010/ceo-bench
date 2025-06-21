#!/usr/bin/env python
"""Quickly check a model by sending a Hello prompt via `llm`."""

import argparse
import subprocess


def call_llm(model: str) -> str:
    result = subprocess.run([
        "llm",
        "prompt",
        "-m",
        model,
        "Hello",
    ], capture_output=True, text=True, check=True)
    return result.stdout.strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Send a hello prompt to a model")
    parser.add_argument("--model", default="gpt-4.1-mini", help="Model name")
    args = parser.parse_args()

    response = call_llm(args.model)
    print(response)


if __name__ == "__main__":
    main()
