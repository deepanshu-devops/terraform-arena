#!/usr/bin/env python3
"""Terraform Arena CLI.

Usage:
  python judge.py list [--level 0] [--difficulty Easy] [--tag aws] [--search s3]
  python judge.py show 1                 # number or stable id
  python judge.py start intro-hcl-blocks
  python judge.py test 1 [--dir workspaces/001-intro-hcl-blocks]
  python judge.py test-all
  python judge.py generate
  python judge.py refresh-starters [--force] [--dry-run]
  python judge.py verify                 # references pass, starters fail
  python judge.py live provision-vpc [--apply --yes]   # gated AWS pilot

The catalog runs from level 0 (HCL fundamentals) to level 5 (capstones).
Every challenge provides complete surrounding code and one focused TODO block.
Default commands run locally and make no cloud calls. ``live`` requires
ARENA_LIVE=1, a sandbox account id, a local AWS profile, and an explicit
--apply --yes for any resource creation.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from app.challenges import all_challenges, get_challenge  # noqa: E402
from app.evaluator import Challenge, evaluate  # noqa: E402
from app.hcl import parse_files  # noqa: E402
from app.workspace import (  # noqa: E402
    WORKSPACES,
    read_workspace,
    refresh_workspace_starters,
    workspace_dir,
    write_workspace,
)

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
DIM = "\033[2m"
BOLD = "\033[1m"
RESET = "\033[0m"


def color(text: str, code: str) -> str:
    if not sys.stdout.isatty():
        return text
    return f"{code}{text}{RESET}"


def _difficulty_color(diff: str) -> str:
    if diff.lower() == "easy":
        return GREEN
    if diff.lower() == "medium":
        return YELLOW
    return RED


def cmd_list(args) -> int:
    challenges = all_challenges()
    if args.level is not None:
        challenges = [c for c in challenges if c.level == args.level]
    if args.difficulty:
        challenges = [c for c in challenges if c.difficulty.lower() == args.difficulty.lower()]
    if args.tag:
        challenges = [c for c in challenges if args.tag.lower() in [t.lower() for t in c.tags]]
    if args.search:
        q = args.search.lower()
        challenges = [
            c
            for c in challenges
            if q in c.title.lower()
            or q in c.id.lower()
            or q in c.scenario.lower()
            or q in c.level_name.lower()
        ]

    print(color(f"{len(challenges)} challenges", BOLD))
    print()
    for c in challenges:
        diff = color(f"{c.difficulty:<6}", _difficulty_color(c.difficulty))
        print(f"{c.number:>3}  L{c.level}  {diff}  {c.title}")
        print(color(f"     {c.id} | {c.points} pts | {', '.join(c.tags)}", DIM))
    return 0


def cmd_show(args) -> int:
    challenge = get_challenge(args.key)
    if not challenge:
        print(f"Challenge {args.key!r} not found.")
        return 1

    print()
    print(color(f"{challenge.number:03d}. {challenge.title}", BOLD))
    print(f"Level: {challenge.level_name or f'Level {challenge.level}'}")
    print(f"Difficulty: {challenge.difficulty} | Points: {challenge.points} | Tags: {', '.join(challenge.tags)}")
    print()
    print(color("SCENARIO", CYAN))
    print(challenge.scenario)
    print()
    focus = challenge.focus or {}
    if focus:
        print(color("WHAT TO COMPLETE", CYAN))
        print(f"  File: {focus.get('file', 'main.tf')}")
        print(f"  Task: {focus.get('title', 'Complete the graded block')}")
        if focus.get("todo"):
            print(f"  {focus['todo']}")
        print()
    print(color("CONSTRAINTS", CYAN))
    for item in challenge.constraints:
        print(f"  - {item}")
    print()
    print(color("INPUT VARIABLES", CYAN))
    if challenge.variables:
        print(f"  {'NAME':<24} {'TYPE':<14} DEFAULT")
        for v in challenge.variables:
            print(f"  {v['name']:<24} {v.get('type', 'string'):<14} {v.get('default', 'required')}")
    else:
        print("  (none)")
    print()
    print(color("EXPECTED OUTPUT RESOURCES", CYAN))
    for r in challenge.expected_resources:
        print(f"  - {r}")
    for o in challenge.expected_outputs:
        print(f"  output: {o}")
    print()
    print(color("HIDDEN TESTS", CYAN))
    print(f"  {len(challenge.tests) + 1} tests (details revealed after a submission)")
    print()
    print(f"Workspace: {workspace_dir(challenge)}")
    print(f"Start with: python judge.py start {challenge.number}")
    return 0


def cmd_start(args) -> int:
    challenge = get_challenge(args.key)
    if not challenge:
        print(f"Challenge {args.key!r} not found.")
        return 1
    folder = write_workspace(challenge, force=args.force)
    print(f"Workspace ready: {folder}")
    for name in challenge.starter:
        print(f"  {name}")
    print()
    print("Open the folder in VS Code, fill in the TODOs, then run:")
    print(f"  python judge.py test {challenge.number}")
    return 0


def _print_result(challenge: Challenge, result: dict) -> None:
    status = result["status"]
    badge = color(f"[{status}]", GREEN if status == "PASS" else RED)
    print()
    print(f"{badge} {challenge.number:03d}. {challenge.title}")
    print(
        f"Score: {result['score']}/100 | Tests: {result['passed']}/{result['total']} "
        f"| {result['duration_ms']} ms"
    )
    print()
    for test in result["tests"]:
        marker = color("PASS", GREEN) if test["passed"] else color("FAIL", RED)
        print(f"  [{marker}] {test['category']:<12} {test['title']}")
        if not test["passed"]:
            print(color(f"         {test['detail']}", DIM))

    security = result["security"]
    print()
    print(color("SECURITY", CYAN))
    if security["blocked"]:
        for item in security["blocked"]:
            print(f"  {color('BLOCKED', RED)} {item}")
    else:
        print("  clean")
    for item in security["warnings"]:
        print(f"  {color('WARN', YELLOW)} {item}")

    fmt = result["formatting"]
    print()
    print(color("FORMATTING", CYAN))
    print(f"  grade {fmt['grade']} ({fmt['score']}/100)")
    for issue in fmt["issues"][:10]:
        print(f"  - {issue}")

    variables = result["variables"]
    print()
    print(color("VARIABLES", CYAN))
    print(f"  grade {variables['grade']} ({variables['score']}/100)")
    for check in variables["checks"]:
        if check["issues"]:
            print(f"  - {check['name']}: {', '.join(check['issues'])}")

    drift = result["drift"]
    print()
    print(color("DRIFT", CYAN))
    if not drift:
        print("  none")
    for item in drift:
        print(f"  - [{item['severity']}] {item['message']}")
    print()


def cmd_test(args) -> int:
    challenge = get_challenge(args.key)
    if not challenge:
        print(f"Challenge {args.key!r} not found.")
        return 1

    folder = Path(args.dir) if args.dir else workspace_dir(challenge)
    if not folder.exists() or not list(folder.glob("*.tf")):
        write_workspace(challenge)
        print(f"Workspace created at {folder}. Fill in the TODOs and re-run.")

    files = read_workspace(folder)
    if not files:
        print(f"No .tf files found in {folder}.")
        return 1

    result = evaluate(challenge, files)
    _print_result(challenge, result)
    return 0 if result["status"] == "PASS" else 1


def cmd_test_all(args) -> int:
    base = Path(args.dir) if args.dir else WORKSPACES
    if not base.exists():
        print(f"No workspace directory: {base}")
        return 1

    passed = failed = skipped = 0
    rows: list[tuple[str, str, int]] = []
    for folder in sorted(base.iterdir()):
        if not folder.is_dir():
            continue
        files = read_workspace(folder)
        if not files:
            skipped += 1
            continue
        try:
            number = int(folder.name.split("-", 1)[0])
        except ValueError:
            skipped += 1
            continue
        challenge = get_challenge(number)
        if not challenge:
            skipped += 1
            continue
        result = evaluate(challenge, files)
        rows.append((folder.name, result["status"], result["score"]))
        if result["status"] == "PASS":
            passed += 1
        else:
            failed += 1

    for name, status, score in rows:
        badge = color(status, GREEN if status == "PASS" else RED)
        print(f"{badge:<12} {score:>3}/100  {name}")
    print()
    print(f"Passed: {passed} | Failed: {failed} | Skipped: {skipped}")
    return 0 if failed == 0 else 1


def cmd_generate(args) -> int:
    from scripts.generate_workspaces import generate

    count = generate(force=args.force)
    print(f"Generated {count} workspaces under {WORKSPACES}")
    return 0


def cmd_refresh_starters(args) -> int:
    updated_total = preserved_total = 0
    touched: list[str] = []
    preserved: list[str] = []

    for challenge in all_challenges():
        updated, kept = refresh_workspace_starters(
            challenge,
            force=args.force,
            dry_run=args.dry_run,
        )
        updated_total += len(updated)
        preserved_total += len(kept)
        if updated:
            touched.append(f"{challenge.number:03d}-{challenge.id}")
        if kept:
            preserved.extend(
                f"{challenge.number:03d}-{challenge.id}/{name}" for name in kept
            )

    verb = "Would update" if args.dry_run else "Updated"
    print(f"{verb} {updated_total} starter files across {len(touched)} workspaces.")
    if args.dry_run:
        print("Would refresh challenge.json metadata in every workspace.")
    else:
        print("Refreshed challenge.json metadata in every workspace.")
    if preserved_total:
        print(f"Preserved {preserved_total} file(s) that contain learner code:")
        for path in preserved:
            print(f"  {path}")
    print("Use --force only when you are sure you want to overwrite learner code.")
    return 0


def cmd_verify(args) -> int:
    """Developer gate: every reference passes and every starter fails."""
    from app.catalog.reference import FOCUS_START

    ref_failures: list[tuple[str, list[str], list[str]]] = []
    starter_failures: list[tuple[str, int]] = []
    parse_failures: list[tuple[str, list[dict]]] = []
    fmt_failures: list[tuple[str, list[str]]] = []
    marker_failures: list[tuple[str, str]] = []
    crashes: list[tuple[str, str]] = []

    # The formatting lesson deliberately ships a badly formatted starter.
    intentional_starter_fmt = {"intro-hcl-formatting"}

    challenges = all_challenges()
    for challenge in challenges:
        cid = challenge.id
        try:
            if not challenge.reference:
                marker_failures.append((cid, "missing reference"))
                continue
            ref_result = evaluate(challenge, challenge.reference)
            if ref_result["status"] != "PASS":
                failed = [
                    t["id"] + ": " + t["detail"]
                    for t in ref_result["tests"]
                    if t["required"] and not t["passed"]
                ]
                ref_failures.append((cid, failed, ref_result["security"]["blocked"]))

            starter_result = evaluate(challenge, challenge.starter)
            if starter_result["status"] != "FAIL":
                starter_failures.append((cid, starter_result["score"]))

            parsed = parse_files(challenge.starter)
            if parsed.errors:
                parse_failures.append((cid, parsed.errors[:3]))

            if (
                starter_result["formatting"]["issues"]
                and cid not in intentional_starter_fmt
            ):
                fmt_failures.append((cid + " starter", starter_result["formatting"]["issues"][:3]))

            joined_starter = "\n".join(challenge.starter.values())
            joined_ref = "\n".join(challenge.reference.values())
            if FOCUS_START in joined_starter:
                marker_failures.append((cid, "focus marker leaked into starter"))
            if FOCUS_START not in joined_ref and cid not in intentional_starter_fmt:
                marker_failures.append((cid, "focus marker missing from reference"))
            focus_file = (challenge.focus or {}).get("file", "main.tf")
            if focus_file not in challenge.starter:
                marker_failures.append((cid, f"focus file missing from starter: {focus_file}"))
        except Exception as exc:  # pragma: no cover - defensive
            import traceback

            crashes.append((cid, traceback.format_exc(limit=4)))

    print(f"challenges: {len(challenges)}")
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
    print(f"formatting failures: {len(fmt_failures)}")
    for cid, errs in fmt_failures:
        print(f"  FMT {cid}: {errs}")
    print(f"marker issues: {len(marker_failures)}")
    for cid, msg in marker_failures:
        print(f"  MARKER {cid}: {msg}")
    print(f"crashes: {len(crashes)}")
    for cid, tb in crashes:
        print(f"  CRASH {cid}")
        print(tb)

    total = (
        len(ref_failures)
        + len(starter_failures)
        + len(parse_failures)
        + len(fmt_failures)
        + len(marker_failures)
        + len(crashes)
    )
    return 0 if total == 0 else 1


def cmd_live(args) -> int:
    import json

    from app.live import LiveError, preflight, print_report, run_live, status

    if args.status:
        print(json.dumps(status(), indent=2))
        return 0
    if args.preflight:
        try:
            ctx = preflight(
                profile=args.profile, region=args.region, account=args.account
            )
        except LiveError as exc:
            print(color(f"[LIVE BLOCKED] {exc}", RED))
            return 2
        print(
            json.dumps(
                {
                    "account": ctx["account"],
                    "arn": ctx["identity"].get("Arn"),
                    "profile": ctx["profile"],
                    "region": ctx["region"],
                    "terraform": ctx["terraform"],
                },
                indent=2,
            )
        )
        return 0
    if not args.key:
        print("Provide a challenge number or id, or use --status / --preflight.")
        return 2
    challenge = get_challenge(args.key)
    if not challenge:
        print(f"Challenge {args.key!r} not found.")
        return 1

    try:
        report = run_live(
            challenge,
            profile=args.profile,
            region=args.region,
            account=args.account,
            apply=args.apply,
            yes=args.yes,
            var_file=args.var_file,
            force=args.force,
            keep=args.keep,
        )
    except LiveError as exc:
        print(color(f"[LIVE BLOCKED] {exc}", RED))
        return 2
    except Exception as exc:  # pragma: no cover - defensive
        print(color(f"[LIVE ERROR] {type(exc).__name__}: {exc}", RED))
        return 3

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print_report(report)
    return 0 if report.get("status") == "PASS" else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Terraform Arena CLI")
    sub = parser.add_subparsers(dest="command")

    p_list = sub.add_parser("list", help="List challenges")
    p_list.add_argument("--level", type=int, choices=range(0, 6))
    p_list.add_argument("--difficulty")
    p_list.add_argument("--tag")
    p_list.add_argument("--search")
    p_list.set_defaults(func=cmd_list)

    p_show = sub.add_parser("show", help="Show a challenge statement")
    p_show.add_argument("key")
    p_show.set_defaults(func=cmd_show)

    p_start = sub.add_parser("start", help="Create the starter workspace")
    p_start.add_argument("key")
    p_start.add_argument("--force", action="store_true")
    p_start.set_defaults(func=cmd_start)

    p_test = sub.add_parser("test", help="Evaluate a workspace")
    p_test.add_argument("key")
    p_test.add_argument("--dir")
    p_test.set_defaults(func=cmd_test)

    p_all = sub.add_parser("test-all", help="Evaluate every workspace")
    p_all.add_argument("--dir")
    p_all.set_defaults(func=cmd_test_all)

    p_gen = sub.add_parser("generate", help="Write all 117 workspace folders")
    p_gen.add_argument("--force", action="store_true")
    p_gen.set_defaults(func=cmd_generate)

    p_refresh = sub.add_parser(
        "refresh-starters",
        help="Update untouched starter files without overwriting learner code",
    )
    p_refresh.add_argument("--force", action="store_true")
    p_refresh.add_argument("--dry-run", action="store_true")
    p_refresh.set_defaults(func=cmd_refresh_starters)

    p_verify = sub.add_parser(
        "verify",
        help="Check that every reference passes and every starter fails",
    )
    p_verify.set_defaults(func=cmd_verify)

    p_live = sub.add_parser(
        "live", help="Plan/apply a challenge in AWS (explicitly gated)"
    )
    p_live.add_argument("key", nargs="?")
    p_live.add_argument("--profile")
    p_live.add_argument("--region")
    p_live.add_argument("--account")
    p_live.add_argument("--var-file")
    p_live.add_argument("--apply", action="store_true")
    p_live.add_argument("--yes", action="store_true")
    p_live.add_argument("--force", action="store_true")
    p_live.add_argument("--keep", action="store_true")
    p_live.add_argument("--json", action="store_true")
    p_live.add_argument("--status", action="store_true")
    p_live.add_argument("--preflight", action="store_true")
    p_live.set_defaults(func=cmd_live)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "command", None):
        parser.print_help()
        return 0
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
