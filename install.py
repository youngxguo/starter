#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path
import sys


REPOSITORY_ROOT = Path(__file__).resolve().parent
SKILLS_ROOT = REPOSITORY_ROOT / "skills"
TARGET_ROOTS = {
    "codex": Path(".agents/skills"),
    "claude": Path(".claude/skills"),
}


class InstallError(Exception):
    pass


class Arguments(argparse.Namespace):
    check: bool = False
    remove: bool = False
    target: list[str] | None = None
    home: Path = Path.home()


def available_skills() -> list[Path]:
    skills = sorted(path for path in SKILLS_ROOT.iterdir() if path.is_dir())
    invalid = [path for path in skills if not (path / "SKILL.md").is_file()]
    if invalid:
        names = ", ".join(path.name for path in invalid)
        raise InstallError(f"skill directories are missing SKILL.md: {names}")
    if not skills:
        raise InstallError("no skills found")
    return skills


def selected_targets(names: list[str] | None) -> dict[str, Path]:
    if not names:
        return TARGET_ROOTS
    return {name: TARGET_ROOTS[name] for name in dict.fromkeys(names)}


def link_status(source: Path, destination: Path) -> str:
    if destination.is_symlink():
        if destination.resolve(strict=False) == source.resolve():
            return "installed"
        return "conflict"
    if destination.exists():
        return "conflict"
    return "missing"


def install(home: Path, target_names: list[str] | None = None) -> None:
    records = installation_records(home, target_names)
    refuse_conflicts(records)

    for tool, source, destination, status in records:
        if status == "installed":
            print(f"{tool}: already installed {source.name}")
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.symlink_to(source, target_is_directory=True)
        print(f"{tool}: linked {source.name} -> {destination}")


def check(home: Path, target_names: list[str] | None = None) -> None:
    records = installation_records(home, target_names)
    refuse_conflicts(records)
    missing = [
        destination for _, _, destination, status in records if status == "missing"
    ]
    if missing:
        formatted = "\n".join(f"  {path}" for path in missing)
        raise InstallError(f"skills are not installed:\n{formatted}")
    for tool, source, _, _ in records:
        print(f"{tool}: installed {source.name}")


def remove(home: Path, target_names: list[str] | None = None) -> None:
    records = installation_records(home, target_names)
    refuse_conflicts(records)

    for tool, source, destination, status in records:
        if status == "missing":
            print(f"{tool}: not installed {source.name}")
            continue
        destination.unlink()
        print(f"{tool}: removed {source.name}")


def installation_records(
    home: Path,
    target_names: list[str] | None,
) -> list[tuple[str, Path, Path, str]]:
    records: list[tuple[str, Path, Path, str]] = []
    for tool, relative_root in selected_targets(target_names).items():
        target_root = home / relative_root
        for source in available_skills():
            destination = target_root / source.name
            records.append(
                (tool, source, destination, link_status(source, destination))
            )
    return records


def refuse_conflicts(records: list[tuple[str, Path, Path, str]]) -> None:
    conflicts = [
        destination for _, _, destination, status in records if status == "conflict"
    ]
    if conflicts:
        formatted = "\n".join(f"  {path}" for path in conflicts)
        raise InstallError(f"refusing to replace existing paths:\n{formatted}")


def parse_arguments() -> Arguments:
    parser = argparse.ArgumentParser(
        description="Link this repository's skills into personal agent directories."
    )
    action = parser.add_mutually_exclusive_group()
    _ = action.add_argument(
        "--check",
        action="store_true",
        help="verify that every selected skill is installed",
    )
    _ = action.add_argument(
        "--remove",
        action="store_true",
        help="remove links created by this repository",
    )
    _ = parser.add_argument(
        "--target",
        action="append",
        choices=sorted(TARGET_ROOTS),
        help="install for only this agent; repeat to select both",
    )
    _ = parser.add_argument(
        "--home", type=Path, default=Path.home(), help=argparse.SUPPRESS
    )
    return parser.parse_args(namespace=Arguments())


def main() -> int:
    arguments = parse_arguments()
    try:
        if arguments.check:
            check(arguments.home, arguments.target)
        elif arguments.remove:
            remove(arguments.home, arguments.target)
        else:
            install(arguments.home, arguments.target)
    except InstallError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
