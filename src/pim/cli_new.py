#!/usr/bin/env python3
import sys
import logging
import argparse
from pim.commands.install import InstallCommand
from pim.commands.list import ListCommand


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s",
    )

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
