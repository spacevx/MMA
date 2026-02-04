import sys

bDisableChaser: bool = False

_BROWSER: bool = sys.platform == "emscripten"


def parse(args: list[str] | None = None) -> None:
    global bDisableChaser

    if _BROWSER:
        bDisableChaser = False
        return

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("--disableChaser", action="store_true")
    parsed = parser.parse_args(args)
    bDisableChaser = parsed.disableChaser
