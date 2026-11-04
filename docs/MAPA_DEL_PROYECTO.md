# Project map — LinguaNova 1.5.5

## Application entry points

| Path | Purpose |
| --- | --- |
| `LinguaNova_Traductor_RenPy.py` | Standalone 1.5.5 application source and default runtime. |
| `run.bat` | Windows source launcher for the 1.5.5 application. |
| `LinguaNova.sh` | Linux/macOS source launcher. |
| `run_cli_1_5_5.py` | CLI wrapper used by the frozen CLI build. |
| `LinguaNova.spec` | PyInstaller configuration for the 1.5.5 GUI and CLI. |
| `COMPILAR_1_5_5.bat` | Standalone Windows build recipe supplied with 1.5.5. |
| `src/version.py` | Shared project/build version metadata. |

## Repository contents

| Path | Purpose |
| --- | --- |
| `src/` | Earlier modular implementation retained for compatibility and regression tests. |
| `locales/` | Interface catalogs used by the modular compatibility implementation. |
| `tests/` | Compatibility regressions plus syntax and CLI smoke tests for 1.5.5. |
| `scripts/` | Repository checks and build helpers. |
| `installer/` | Windows installer definition and localization. |
| `linguanova_next/` | Separate experimental generation; not the default application. |
| `.github/` | Automated tests, release workflows, and repository templates. |
| `docs/` | User instructions, release notes, and maintenance documentation. |

## Maintenance notes

The default launcher and GUI release build use the self-contained 1.5.5
source file. Do not edit `src/` expecting those changes to alter that runtime;
the modular tree remains for compatibility and its existing regression suite.
The CLI frozen build uses `run_cli_1_5_5.py` to invoke the same standalone
source with `--cli`.

The original patch bundled with the 1.5.5 ZIP does not apply cleanly to the
current modular tree. It is not used as a build input. The source file,
version metadata, launchers, and build entry points are updated independently.

## Validate

Run the release-source checks and core regressions with:

```bash
python -m pytest -q tests/test_release_source_155.py
```

Run the full repository suite with:

```bash
python -m pytest -q
```

The test suite includes older modular compatibility checks. A successful
syntax or CLI smoke test does not certify translations against every Ren'Py
game or prove the Windows executable builds on every machine.
