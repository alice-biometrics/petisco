import argparse
import os

from petisco import __version__


def has_args(args):
    is_active = False
    for arg in vars(args):
        is_active = is_active or getattr(args, arg)
    return is_active


def rename_template(original_name: str, replacement: str):

    for dname, _, _ in os.walk("."):
        if original_name in dname:
            os.rename(dname, dname.replace(original_name, replacement))

    blacklist = [".git/", ".idea"]
    for dname, dirs, files in os.walk("."):
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


def main():
    parser = argparse.ArgumentParser(
        prog="petisco 🍪",
        description="petisco is a framework for helping Python developers to build clean Applications",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-v", "--version", action="store_true", help="show petisco version number."
    )
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

        if args.rename_template_replacement:
            print(
                f"petisco 🍪 => Changing {args.original_template_name} for {args.rename_template_replacement}..."
            )
            rename_template(
                args.original_template_name, args.rename_template_replacement
            )
            return
