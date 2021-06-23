import argparse
import asyncio
import pathlib

from opencicd.exec_plan import create_graph, execute_plan


def run(args: argparse.Namespace) -> None:
    spec_file = pathlib.Path(args.spec_file)
    if not spec_file.is_file():
        raise RuntimeError(f"Can't find spec-file {spec_file}")
    try:
        work_dir = spec_file.parents[0].absolute()
    except IndexError:
        raise RuntimeError(f"Can't find spec-file directory {spec_file}")
    execution_graph = create_graph(spec_file)
    asyncio.run(execute_plan(execution_graph, work_dir))


def main() -> None:
    """
    Commands:
        - run --spec-file=.opencicd.yml — runs CI/CD commands from spec_file
    :return:
    """
    parser = argparse.ArgumentParser(description="OpenSource CI/CD tool")

    subparsers = parser.add_subparsers(help="select action")
    parser_run = subparsers.add_parser("run")
    parser_run.add_argument(
        "--spec-file", default=".opencicd.yaml"
    )
    parser_run.set_defaults(func=run)
    cli_args = parser.parse_args()
    cli_args.func(cli_args)


if __name__ == "__main__":
    main()
