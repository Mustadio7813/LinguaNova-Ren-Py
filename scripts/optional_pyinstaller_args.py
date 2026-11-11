"""Print PyInstaller hidden-import arguments for installed optimizer modules."""
import importlib.util


OPTIONAL_IMPORTS = (
    ("PIL", "PIL.Image"),
    ("oxipng", "oxipng"),
    ("imagequant", "imagequant"),
    ("mozjpeg_lossless_optimization", "mozjpeg_lossless_optimization"),
)


def main():
    arguments = []
    for package, module in OPTIONAL_IMPORTS:
        try:
            if importlib.util.find_spec(package) is not None:
                arguments.extend(("--hidden-import", module))
        except (ImportError, ValueError):
            continue
    print(" ".join(arguments))


if __name__ == "__main__":
    main()
