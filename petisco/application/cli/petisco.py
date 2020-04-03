import argparse

from petisco import __version__


def has_args(args):
    is_active = False
    for arg in vars(args):
        is_active = is_active or getattr(args, arg)
    return is_active


def main():
    parser = argparse.ArgumentParser(
        prog="petisco 🍪",
        description="petisco is a framework for helping Python developers to build clean Applications",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-v", "--version", action="store_true", help="show petisco version number."
    )

    args = parser.parse_args()

    if not has_args(args):
        parser.print_help()
    else:
        if args.version:
            print(f"petisco 🍪 => {__version__}")
            return
