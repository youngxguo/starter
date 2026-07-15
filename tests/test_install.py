#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
INSTALLER = REPOSITORY_ROOT / "install.py"
SKILL_NAMES = {path.name for path in (REPOSITORY_ROOT / "skills").iterdir()}


class InstallTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory(
            prefix="skills-install-test."
        )
        self.home = Path(self.temporary_directory.name)

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def run_installer(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(INSTALLER),
                "--home",
                str(self.home),
                *arguments,
            ],
            text=True,
            capture_output=True,
            check=False,
        )

    def destinations(self, tool: str) -> list[Path]:
        directory = ".agents" if tool == "codex" else ".claude"
        return [self.home / directory / "skills" / name for name in SKILL_NAMES]

    def test_installs_every_skill_for_codex_and_claude(self) -> None:
        result = self.run_installer()

        self.assertEqual(result.returncode, 0, result.stderr)
        for tool in ("codex", "claude"):
            for destination in self.destinations(tool):
                self.assertTrue(destination.is_symlink())
                self.assertEqual(
                    destination.resolve(),
                    (REPOSITORY_ROOT / "skills" / destination.name).resolve(),
                )

    def test_install_is_idempotent(self) -> None:
        self.assertEqual(self.run_installer().returncode, 0)

        result = self.run_installer()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("already installed", result.stdout)

    def test_check_reports_missing_and_then_installed(self) -> None:
        missing = self.run_installer("--check")
        self.assertEqual(missing.returncode, 1)
        self.assertIn("skills are not installed", missing.stderr)

        self.assertEqual(self.run_installer().returncode, 0)
        installed = self.run_installer("--check")
        self.assertEqual(installed.returncode, 0, installed.stderr)

    def test_conflict_prevents_all_changes(self) -> None:
        conflict = self.destinations("codex")[0]
        conflict.parent.mkdir(parents=True)
        conflict.write_text("keep me\n")

        result = self.run_installer()

        self.assertEqual(result.returncode, 1)
        self.assertIn("refusing to replace", result.stderr)
        self.assertEqual(conflict.read_text(), "keep me\n")
        for destination in self.destinations("claude"):
            self.assertFalse(destination.exists())

    def test_remove_deletes_only_its_links(self) -> None:
        self.assertEqual(self.run_installer().returncode, 0)

        result = self.run_installer("--remove")

        self.assertEqual(result.returncode, 0, result.stderr)
        for tool in ("codex", "claude"):
            for destination in self.destinations(tool):
                self.assertFalse(destination.is_symlink())

    def test_can_target_only_codex(self) -> None:
        result = self.run_installer("--target", "codex")

        self.assertEqual(result.returncode, 0, result.stderr)
        for destination in self.destinations("codex"):
            self.assertTrue(destination.is_symlink())
        for destination in self.destinations("claude"):
            self.assertFalse(destination.exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
