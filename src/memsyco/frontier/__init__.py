"""Frontier tests F1-F4, kept apart from the main study. Design, files and run steps: frontier/README.md.

Prompt wording used only by these tests lives in `frontier/prompts/`, not in the main study's
`memsyco/prompts/`, so no main-study prompt can change by accident.
"""

from functools import cache
from importlib import resources


@cache
def prompt(name: str) -> str:
    return resources.files("memsyco.frontier.prompts").joinpath(f"{name}.txt").read_text(encoding="utf-8")
