#!/usr/bin/env python3
import sys
import logging
import argparse
from pim.commands.install import InstallCommand
from pim.commands.list import ListCommand
from pim.utils.logging_filter import RelativePathFilter


def main():
    # The format string now uses %(relpath)s, which is added by our custom filter.
    log_format = "[%(levelname)s:%(relpath)s:%(lineno)d] %(message)s"
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
    )
    # Add the custom filter to the root logger to create the relative path
    logging.getLogger().addFilter(RelativePathFilter())

    commands = {"install": InstallCommand(), "list": ListCommand()}

    parser = argparse.ArgumentParser(
        description="A CLI to declaratively install and manage machine learning models from a Pimfile."
    )
    subparsers = parser.add_subparsers(
        dest="command", help="Available commands", required=True
    )

    # Add all commands
    for cmd in commands.values():
        cmd_parser = subparsers.add_parser(cmd.name, help=cmd.description)
        cmd.parser = cmd_parser
        cmd.add_arguments()

    args = parser.parse_args()
    return commands[args.command].run(args)


if __name__ == "__main__":
    sys.exit(main())
