import argparse
import importlib.util
import inspect
import sys
from typing import Any

from loguru import logger


def has_args(args: Any) -> bool:
    is_active = False
    for arg in vars(args):
        is_active = is_active or getattr(args, arg)
    return is_active


def get_application(module_path: str):
    logger.remove()
    logger.add(sys.stderr, level="ERROR")

    try:
        module_name = importlib.import_module(module_path)
        application = getattr(module_name, "application")
        return application
    except Exception as exc:  # noqa
        print(
            f"Error loading the app module. Impossible to extract information from {module_path}. "
            f"There is no application instance in {module_path}"
        )
        print(
            "Try to install your app module with `pip install -e .` (maybe you need to add a setup.py or a "
            "pyproject.toml to your app root"
        )
        if is_rich_available():
            from rich.console import Console

            console = Console()
            console.print_exception()
        else:
            print(str(exc))


def encourage_rich_installation() -> None:
    print(
        "\n⚠️ If you want to represent this info in a fancy way. Try to install rich or just install petisco[rich]"
    )


def is_rich_available() -> bool:
    try:
        import rich  # noqa
    except (RuntimeError, ImportError):
        return False
    return True


def show_info(application) -> None:
    dependencies = application.dependencies_provider()
    configurers = application.configurers

    if is_rich_available() is False:
        print("Petisco Application:")
        print(f"name: {application.name}")
        print(f"version: {application.version}")
        print(f"organization: {application.organization}")
        print(f"deployed_at: {application.deployed_at}")
        print(f"dependencies: {len(dependencies)}")
        print(f"configurers: {len(configurers)}")
        encourage_rich_installation()
    else:
        from rich import print
        from rich.panel import Panel

        panel = Panel.fit(
            f"[bold]name:         [/] {application.name}\n"
            f"[bold]version:      [/] {application.version}\n"
            f"[bold]organization: [/] {application.organization}\n"
            f"[bold]deployed_at:  [/] {application.deployed_at}\n"
            f"[bold]dependencies: [/] {len(dependencies)}\n"
            f"[bold]configurers:  [/] {len(configurers)}",
            title="Petisco Application",
        )
        print(panel)


def show_dependencies(application) -> None:
    dependencies = application.dependencies_provider()

    if is_rich_available() is False:
        print("Dependencies:")
        for dependency in dependencies:
            text = f"{dependency.type.__name__} -> "
            for key, builder in dependency.builders.items():
                text += f"{key}: {builder.klass.__name__} | "
            text = text[:-2]
            print(text)
        encourage_rich_installation()
    else:
        from rich.console import Console
        from rich.table import Table

        table = Table()
        console = Console()

        table.add_column("Type", justify="right", style="cyan", no_wrap=True)
        table.add_column("Default")
        table.add_column("Implementations", style="green")
        table.add_column("ENV", style="red")

        for dependency in dependencies:
            type = dependency.get_key()
            default_implementation = dependency.builders.pop("default").klass.__name__

            implementations = ""
            for key, builder in dependency.builders.items():
                implementations += f"{key}: {builder.klass.__name__}\n"
            implementations = implementations[:-1]

            table.add_row(
                type, default_implementation, implementations, dependency.envar_modifier
            )

        console.print(table)


def show_configurers(application) -> None:
    configurers = application.configurers

    if is_rich_available() is False:
        print("Configurers:")
        for configurer in configurers:
            print(
                f"{configurer.__class__.__name__} -> {configurer.execute_after_dependencies=}"
            )
        encourage_rich_installation()
    else:
        from rich.console import Console
        from rich.table import Table

        table = Table()
        console = Console()

        table.add_column("Configurer", justify="right", style="cyan", no_wrap=True)
        table.add_column("execute_after_dependencies", justify="center")

        for configurer in configurers:
            table.add_row(
                configurer.__class__.__name__,
                str(configurer.execute_after_dependencies),
            )

        console.print(table)


def show_sql_models(declarative_base_path: str) -> None:
    module_name, class_name = declarative_base_path.rsplit(".", 1)
    module = importlib.import_module(module_name)
    Base = getattr(module, class_name)

    info: list[dict[str, str]] = []
    for sql_model in Base.__subclasses__():
        info.append(
            {
                "name": sql_model.__name__,
                "module": sql_model.__module__,
                "filename": inspect.getsourcefile(sql_model),
            }
        )

    if is_rich_available() is False:
        print(info)
    else:
        from rich.console import Console
        from rich.table import Table

        table = Table()
        console = Console()

        table.add_column("Model", justify="right", style="cyan", no_wrap=True)
        table.add_column("Filename", justify="left")

        for model_info in info:
            filename = model_info.get("filename")
            table.add_row(
                model_info.get("name"),
                f"file://{filename}",
            )
        console.print(table)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="petisco-dev 🍪",
        description="petisco dev tools to inspect your application",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-i", "--info", action="store_true", help="show petisco app info."
    )
    parser.add_argument(
        "-deps",
        "--dependencies",
        action="store_true",
        help="show petisco app dependencies.",
    )
    parser.add_argument(
        "-configs",
        "--configurers",
        action="store_true",
        help="show petisco app configurers.",
    )
    parser.add_argument(
        "-sql-models",
        "--sql-models",
        action="store_true",
        help="show petisco sql models.",
    )
    parser.add_argument(
        "-declarative-base",
        "--declarative-base",
        default="petisco.extra.sqlalchemy.SqlBase",
        help="path to DeclarativeBase, a class to gather all the SQL models",
    )
    parser.add_argument(
        "--application",
        default="app.application",
        help="Module path (default app.application)",
    )

    args = parser.parse_args()

    if not has_args(args):
        parser.print_help()
    else:
        application = get_application(args.application)
        if application is None:
            return

        if args.info:
            show_info(application)
            return

        if args.dependencies:
            show_dependencies(application)
            return

        if args.configurers:
            show_configurers(application)
            return

        if args.sql_models:
            show_sql_models(args.declarative_base)
            return
