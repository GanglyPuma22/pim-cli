from argparse import ArgumentParser


class BaseCommand:
    """Base class for all pim commands"""

    name = None  # Command name
    description = None  # Command description

    def __init__(self) -> None:
        self.parser = ArgumentParser()

    def add_arguments(self) -> None:
        """Add command-specific arguments"""
        pass

    def run(self, args) -> int:
        """Execute the command"""
        raise NotImplementedError()
