#!/usr/bin/env python3
import os
import sys
import logging
import argparse
from pim.commands.install import InstallCommand
from pim.commands.list import ListCommand
from pim.cli_utils.console import init_console
from pim.cli_utils.logging_setup import setup_logger


def main():

    commands = {"install": InstallCommand(), "list": ListCommand()}

    parser = argparse.ArgumentParser(
        description="A CLI to declaratively install and manage machine learning models from a Pimfile."
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        default=False,
        help="Set logging level to DEBUG and print to console",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        default=True if "NO_COLOR" in os.environ else False,
        help="Disable colored output in terminal",
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
    # Set up logging first, since console logs with it
    setup_logger(debug=args.debug)
    init_console(no_color=args.no_color, debug=args.debug)

    return commands[args.command].run(args)


if __name__ == "__main__":
    sys.exit(main())
