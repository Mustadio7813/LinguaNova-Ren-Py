# SPDX-License-Identifier: GPL-3.0-or-later
from pathlib import Path
import re
import shlex
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


def test_optimizer_feature_is_in_release_source_and_documented():
    source = Path("LinguaNova_Traductor_RenPy.py").read_text(encoding="utf-8")
    assert "LN_src_tools_game_optimizer__compress" in source
    assert "LN_src_backend_optimizer_backend__OptimizerBackend" in source
    assert "LN_RESOURCE_src_gui_qml_components_OptimizeGameCard_qml" in source
    assert Path("docs/ALIGERAR_JUEGO.md").is_file()
    assert Path("docs/PRUEBA_ALIGERAR_JUEGO.py").is_file()
    assert Path("COMPILAR_PORTABLE.bat").is_file()


def test_optional_optimizer_imports_are_only_selected_when_available():
    result = subprocess.run(
        [sys.executable, "scripts/optional_pyinstaller_args.py"],
        capture_output=True,
        check=False,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
    arguments = shlex.split(result.stdout)
    assert len(arguments) % 2 == 0
    assert all(arguments[index] == "--hidden-import" for index in range(0, len(arguments), 2))
    assert set(arguments[1::2]) <= {
        "PIL.Image",
        "oxipng",
        "imagequant",
        "mozjpeg_lossless_optimization",
    }


def test_latest_source_cli_help_starts_without_network_access():
    result = subprocess.run(
        [sys.executable, "LinguaNova_Traductor_RenPy.py", "--cli", "--help"],
        capture_output=True,
        check=False,
        timeout=90,
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
