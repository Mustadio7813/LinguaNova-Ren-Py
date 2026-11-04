# SPDX-License-Identifier: GPL-3.0-or-later
from pathlib import Path
import re
import subprocess
import sys


def test_latest_source_is_python_and_reports_155():
    source_path = Path("LinguaNova_Traductor_RenPy.py")
    source = source_path.read_text(encoding="utf-8")

    compile(source, str(source_path), "exec")
    assert re.search(r"VERSION\s*=\s*['\"]1\.5\.5['\"]", source)


def test_release_pages_show_latest_version():
    for readme in ("README.md", "README.es.md"):
        assert "1.5.5" in Path(readme).read_text(encoding="utf-8")


def test_project_version_and_default_launchers_target_latest_source():
    from src.version import VERSION

    assert VERSION == "1.5.5"
    assert "LinguaNova_Traductor_RenPy.py" in Path("run.bat").read_text(
        encoding="utf-8"
    )
    assert "['LinguaNova_Traductor_RenPy.py']" in Path("LinguaNova.spec").read_text(
        encoding="utf-8"
    )


def test_latest_source_cli_help_starts_without_network_access():
    result = subprocess.run(
        [sys.executable, "LinguaNova_Traductor_RenPy.py", "--cli", "--help"],
        capture_output=True,
        check=False,
        timeout=30,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "LinguaNova CLI v1.5.5" in result.stdout


def test_frozen_cli_wrapper_help_starts_without_network_access():
    result = subprocess.run(
        [sys.executable, "run_cli_1_5_5.py", "--help"],
        capture_output=True,
        check=False,
        timeout=30,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "LinguaNova CLI v1.5.5" in result.stdout
