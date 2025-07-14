import argparse
import logging
import os
from pathlib import Path
from .base import BaseCommand
from ..util.pimfile_parser import load_pimfile
from ..util.pathing import find_pimfile, get_cache_dir

class ValidateCachePathAction(argparse.Action):
    def __call__(self, parser, namespace, string_path, option_string=None):
        cache_path = Path(string_path)
        cache_path.mkdir(parents=True, exist_ok=True)
        #Resolve entire path to ensure it's absolute
        setattr(namespace, self.dest, cache_path.resolve())

class ValidateFilePathAction(argparse.Action):
    def __call__(self, parser, namespace, string_path, option_string=None):
        path = Path(string_path)
        if not path.exists():
            parser.error(f"File not found: {path}")
        if not path.is_file():
            parser.error(f"Path is not a file: {path}")
        setattr(namespace, self.dest, path.resolve())

def validate_path(path_str):
    return os.path.abspath(path_str)

class InstallCommand(BaseCommand):
    name = "install"
    description = "Install models from a Pimfile"

    def add_arguments(self) -> None:
        self.parser.add_argument(
            "models",
            nargs="*",  # Allow zero or more model names
            help="Optional: Specific models to install (e.g., framework1:model_name1 framework2:model_name2)"
        )
        self.parser.add_argument(
            "--auth", 
            action="store_true", 
            help="Use Hugging Face token for private models"
        )
        self.parser.add_argument(
            "-f", 
            "--file",
            default=None,
            action=ValidateFilePathAction,
            help="Path to the Pimfile, if not specified will walk up the directory tree to find it."
        )
        self.parser.add_argument(
            "--cache-dir", 
            default=get_cache_dir(),
            action=ValidateCachePathAction, #Resolve full path when user specified
            help="Specify where to save the models (default: ~/.pim/cache)"
        )
    def run(self, args) -> int:
        try:
            #Check if models list is empty
            if not args.models or args.file:
                pimfile_path = find_pimfile() if args.file is None else Path(args.file)
                logging.info(f"Installing models from {pimfile_path} and saving to {args.cache_dir}")
                print(f"{pimfile_path.resolve()}") #Temp statement
            
            if args.models:
                print(f"Models requested: {args.models}")
        except Exception as e:
            logging.error(e)
            return 1