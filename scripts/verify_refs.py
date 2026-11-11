"""Developer check: every generated reference passes, every starter fails."""
from __future__ import annotations

import sys
import traceback

sys.path.insert(0, ".")

from app.catalog.extra import all_specs
from app.catalog.reference import (
    FOCUS_START,
    build_reference,
    choose_focus,
    render_starter,
)
from app.declarative import build_challenge
from app.evaluator import evaluate
from app.hcl import parse_files


def main() -> int:
    ref_failures = []
    starter_failures = []
    parse_failures = []
    fmt_failures = []
    marker_failures = []
    crash = []

    specs = list(all_specs())
    for spec in specs:
        cid = spec.get("id", "?")
        try:
            challenge = build_challenge(spec, 0)
            reference = build_reference(spec)
            starter = render_starter(spec)
            focus = choose_focus(spec)

            ref_result = evaluate(challenge, reference)
            if ref_result["status"] != "PASS":
                failed = [
                    t["id"] + ": " + t["detail"]
                    for t in ref_result["tests"]
                    if t["required"] and not t["passed"]
                ]
                ref_failures.append((cid, failed, ref_result["security"]["blocked"]))

            st_result = evaluate(challenge, starter)
            if st_result["status"] != "FAIL":
                starter_failures.append((cid, st_result["score"]))

            parsed = parse_files(starter)
            if parsed.errors:
                parse_failures.append((cid, parsed.errors[:3]))

            if st_result["formatting"]["issues"] and not spec.get("starter_override"):
                fmt_failures.append((cid, st_result["formatting"]["issues"][:3]))

            joined_start = "\n".join(starter.values())
            joined_ref = "\n".join(reference.values())
            if FOCUS_START in joined_start:
                marker_failures.append((cid, "marker leaked into starter"))
            if FOCUS_START not in joined_ref and not spec.get("starter_override"):
                marker_failures.append((cid, "marker missing from reference"))
            if focus.file not in starter:
                marker_failures.append((cid, f"focus file missing: {focus.file}"))
        except Exception:
            crash.append((cid, traceback.format_exc(limit=4)))

    print(f"specs: {len(specs)}")
    print(f"reference failures: {len(ref_failures)}")
    for cid, failed, blocked in ref_failures:
        print(f"  REF FAIL {cid}")
        for item in failed[:12]:
            print(f"    - {item}")
        for item in blocked:
            print(f"    ! {item}")
    print(f"starter unexpectedly passing: {len(starter_failures)}")
    for cid, score in starter_failures:
        print(f"  STARTER PASS {cid} ({score})")
    print(f"starter parse failures: {len(parse_failures)}")
    for cid, errs in parse_failures:
        print(f"  PARSE {cid}: {errs}")
    print(f"starter formatting failures: {len(fmt_failures)}")
    for cid, errs in fmt_failures:
        print(f"  FMT {cid}: {errs}")
    print(f"marker issues: {len(marker_failures)}")
    for cid, msg in marker_failures:
        print(f"  MARKER {cid}: {msg}")
    print(f"crashes: {len(crash)}")
    for cid, tb in crash:
        print(f"  CRASH {cid}")
        print(tb)

    total = (
        len(ref_failures)
        + len(starter_failures)
        + len(parse_failures)
        + len(fmt_failures)
        + len(marker_failures)
        + len(crash)
    )
    return 0 if total == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
