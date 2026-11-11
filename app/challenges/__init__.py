"""Challenge registry: hand-authored capstones plus the generated catalog."""
from __future__ import annotations

from ..catalog import load_catalog
from ..catalog.reference import LEVEL_NAMES, canonicalize_files, mask_reference
from ..evaluator import Challenge
from . import asg, docker, s3, serverless, vpc
from .solutions import FOCUS, REFERENCES

BUILTIN: list[Challenge] = [
    s3.CHALLENGE,
    docker.CHALLENGE,
    vpc.CHALLENGE,
    asg.CHALLENGE,
    serverless.CHALLENGE,
]

# Capstones are level 5.  Each ships a complete reference solution and masks
# exactly one block to form the learner starter.
for _challenge in BUILTIN:
    _challenge.level = 5
    _challenge.level_name = LEVEL_NAMES[5]
    _challenge.reference = canonicalize_files(REFERENCES[_challenge.id])
    _challenge.focus = FOCUS[_challenge.id]
    _challenge.starter = canonicalize_files(
        mask_reference(_challenge.reference, _challenge.focus)
    )

_REGISTRY: list[Challenge] | None = None


def all_challenges() -> list[Challenge]:
    global _REGISTRY
    if _REGISTRY is None:
        merged = list(BUILTIN) + list(load_catalog())
        merged.sort(key=lambda c: (c.level, c.points, c.title))
        for index, challenge in enumerate(merged, start=1):
            challenge.number = index
        _REGISTRY = merged
    return _REGISTRY


def get_challenge(key: str | int | None) -> Challenge | None:
    if key is None or key == "":
        return None
    text = str(key)
    for challenge in all_challenges():
        if str(challenge.number) == text or challenge.id == text:
            return challenge
    return None


def challenge_by_number(number: int) -> Challenge | None:
    for challenge in all_challenges():
        if challenge.number == number:
            return challenge
    return None


def challenge_count() -> int:
    return len(all_challenges())
