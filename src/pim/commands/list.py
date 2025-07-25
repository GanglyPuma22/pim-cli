import logging
from pathlib import Path
from pim.commands.base import BaseCommand


class ListCommand(BaseCommand):
    name = "list"
    description = "List models defined in a Pimfile"

    def add_arguments(self) -> None:
        self.parser.add_argument(
            "-f",
            "--file",
            default="Pimfile",
            help="Path to the Pimfile (default: ./Pimfile)",
        )

    def run(self, args) -> int:
        try:
            pimfile_path = Path(args.file)
            # ...existing list logic...
            return 0
        except Exception as e:
            logging.error(e)
            return 1
