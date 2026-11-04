# LinguaNova 1.5.5

**English** · [Español](README.es.md)

LinguaNova 1.5.5 is a Ren'Py game translator. This source release uses a
self-contained Python entry point and preserves Ren'Py syntax, variables,
placeholders, and text tags while creating translated language files.

> [!WARNING]
> The program writes translation files into the selected game. Back up the
> game first and test on a copy. Translation quality and compatibility with
> every game or execution path are not guaranteed. This version does not use
> OCR to translate text embedded in images.

> [!IMPORTANT]
> LinguaNova is an independently maintained modified work based in part on
> RenLocalizer 2.8.19. It is not an official RenLocalizer release and is not
> affiliated with, endorsed, or supported by its original authors.
>
> Original project: https://github.com/Lord0fTurk/RenLocalizer
>
> Preserved upstream copyright: Copyright (C) 2025 RenLocalizer V2 Authors
>
> License: GNU GPL v3 or later (**GPL-3.0-or-later**)
> See [NOTICE.md](NOTICE.md), [UPSTREAM.md](UPSTREAM.md),
> [LICENSE_POLICY.md](LICENSE_POLICY.md), and
> [MODIFICATIONS_LINGUANOVA.md](MODIFICATIONS_LINGUANOVA.md).

![Python](https://img.shields.io/badge/Python-3.10%2B-3776ab?style=flat-square&logo=python&logoColor=white)
![Ren'Py](https://img.shields.io/badge/Ren'Py-7%20%26%208-ffb86b?style=flat-square)
![License](https://img.shields.io/badge/License-GPL--3.0--or--later-111827?style=flat-square)

## Quick start

1. Make a backup or copy of the Ren'Py game.
2. Download or clone this repository and extract it to a regular folder.
3. Install Python 3.10 or later if it is not already installed.
4. On Windows, run `run.bat`. On Linux or macOS, run
   `python3 LinguaNova_Traductor_RenPy.py` (or `./LinguaNova.sh`).
5. Select the game folder or supported executable, choose the source and target
   languages and engine, then start translation. Review the result in the
   game before sharing it.

The first source launch may create an isolated environment and download
dependencies. Internet access is required for this setup and for online
translation engines.

## What is included

- Ren'Py translation with protected variables, placeholders, and text tags.
- Analysis of supported `.rpy`, `.rpyc`, and packed game content.
- Translation review and manual corrections.
- Interface-language MOD tools and in-app corrections.
- A work queue, progress reporting, cancellation, and recovery of interrupted
  work.
- DeepL API-key controls and translation engines provided by the application.
- English, Spanish, French, Portuguese, and Russian interface catalogs.
- Verified backups stored outside the game's `game/` folder and a recovery
  command for the latest operation.

The MOD workflow is separate from the main translation. A game is not
guaranteed to launch correctly just because text preparation completed; the
application reports pending text and verification warnings.

## Cancel and restore

Use the in-app **Stop** control once and allow the current operation to save
and finish its cleanup. Do not terminate the process while it is writing.

To restore the verified backup of the latest operation:

```text
python LinguaNova_Traductor_RenPy.py --restaurar "GAME_FOLDER" --idioma spanish
```

Close the game before restoring. Recovery checks the recorded game path and
file hashes, and refuses to overwrite files that changed after the operation.
See [the 1.5.5 user guide](docs/LEEME_1_5_5.md) and the
[recovery notes](docs/ARREGLO_CANCELACION_1_5_5.md).

## DeepL

Select DeepL on the Translation page, enter the API key, and use **Save**.
The key is stored in the local user configuration, not in the source code or
the compiled executable. See
[DeepL and build notes](docs/ARREGLO_DEEPL_Y_COMPILACION_1_5_5.md).

## Source and builds

The 1.5.5 application source is [`LinguaNova_Traductor_RenPy.py`](LinguaNova_Traductor_RenPy.py).
The older modular source and its regression suite remain in the repository
for compatibility and maintenance; the default Windows launcher and release
GUI build target the 1.5.5 entry point.

- Windows source launch: `run.bat`
- Windows portable-folder build: `build_windows.bat`
- Windows installer: `build_installer.bat` (requires Inno Setup 6.5+)
- Direct Windows build of the standalone source: `COMPILAR_1_5_5.bat`
- CLI help: `python LinguaNova_Traductor_RenPy.py --cli --help`

The ZIP contains historical test reports from a trial build; they are not a
substitute for running this repository's tests against the exact source here.
The Windows executable and a user's game must be tested on their intended
systems. See the included [1.5.5 guide](docs/LEEME_1_5_5.md) for limitations.

## Contributing and validation

The modular compatibility suite can be run with:

```bash
python -m pytest -q
```

The latest standalone source is syntax-checked by the release regression
test. Please report issues with the game's Ren'Py version, the relevant log,
and steps to reproduce; do not attach copyrighted game files.

## License

LinguaNova is distributed under **GNU GPL-3.0-or-later**. See
[LICENSE](LICENSE), [COPYING](COPYING), [NOTICE.md](NOTICE.md), and
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). No non-commercial
restriction is added.
