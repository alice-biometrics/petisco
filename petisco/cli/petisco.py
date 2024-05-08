import argparse
import os
from datetime import datetime, timezone
from typing import Any

from petisco import __version__
from petisco.base.domain.model.uuid import Uuid


def has_args(args: Any) -> bool:
    is_active = False
    for arg in vars(args):
        is_active = is_active or getattr(args, arg)
    return is_active


def rename_template(original_name: str, replacement: str) -> None:
    for dname, _, _ in os.walk("."):
        if original_name in dname:
            os.rename(dname, dname.replace(original_name, replacement))

    blacklist = [".git/", ".idea"]
    for dname, _dirs, files in os.walk("."):
        for fname in files:
            fpath = os.path.join(dname, fname)
            rewrite = True
            for blackfolder in blacklist:
                if blackfolder in fpath:
                    rewrite = False
            if rewrite is False:
                continue
            try:
                with open(fpath) as f:
                    s = f.read()
                s = s.replace(original_name, replacement)
                with open(fpath, "w") as f:
                    f.write(s)
            except Exception:
                pass


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="petisco 🍪",
        description="petisco is a framework for helping Python developers to build clean Applications",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("-v", "--version", action="store_true", help="show petisco version number.")
    parser.add_argument("-uuid", "--uuid", action="store_true", help="show an UUID v4.")
    parser.add_argument("-utcnow", "--utcnow", action="store_true", help="show a utc now datetime")
    parser.add_argument(
        "-rt",
        "--rename-template",
        action="store",
        dest="rename_template_replacement",
        default=None,
        help="Rename a petisco service template.",
    )
    parser.add_argument(
        "-tn",
        "--original-template-name",
        action="store",
        dest="original_template_name",
        default="taskmanager",
        help="Rename a petisco service template.",
    )

    args = parser.parse_args()

    if not has_args(args):
        parser.print_help()
    else:
        if args.version:
            print(f"petisco 🍪 => {__version__}")
            return

        if args.uuid:
            print(Uuid.v4().value)
            return

        if args.utcnow:
            print(datetime.now(timezone.utc))
            return

        if args.rename_template_replacement:
            print(
                f"petisco 🍪 => Changing {args.original_template_name} for {args.rename_template_replacement}..."
            )
            rename_template(args.original_template_name, args.rename_template_replacement)
            return
