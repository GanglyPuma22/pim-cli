import argparse
import logging
import os
from pathlib import Path
from .base import BaseCommand
from ..util.model_parsing import parse_models_list, parse_pimfile
from ..util.pathing import find_pimfile, validate_cache_path, validate_file_path


class InstallCommand(BaseCommand):
    """
    Install packages from:

    - HuggingFace
    - TorchVision
    - Scikit-learn
    - Local directories.
    - Git repositories.

    pim also supports installing from "Pimfile files", which provide
    an easy way to specify a whole environment to be installed.
    """

    name = "install"
    description = "Install models from a Pimfile"

    def add_arguments(self) -> None:
        self.parser.add_argument(
            "models",
            nargs="*",  # Allow zero or more model names
            help="Optional: Specific models to install (e.g., framework1:model_name1 framework2:model_name2)",
        )
        self.parser.add_argument(
            "--auth",
            action="store_true",
            help="Use Hugging Face token for private models",
        )
        self.parser.add_argument(
            "--isolated",
            action="store_false",
            help="Do not use base conda enviornment but instead use an isolated environment PER model",
        )
        self.parser.add_argument(
            "-f",
            "--file",
            default=None,
            help="Path to the Pimfile, if not specified will walk up the directory tree to find it.",
        )
        self.parser.add_argument(
            "--cache-dir",
            default=None,
            help="Specify where to save the models (default: ~/.pim/cache)",
        )

    def run(self, args) -> int:
        try:
            cache_dir = validate_cache_path(args.cache_dir)
            # Check if models list is empty
            if not args.models or args.file:
                pimfile_path = (
                    find_pimfile()
                    if args.file is None
                    else validate_file_path(args.file)
                )
                logging.info(
                    f"Installing models from {pimfile_path} and saving to {cache_dir}"
                )
                print(f"{pimfile_path.resolve()}")  # Temp statement
                # TODO Update parser to handle dependencies too and python version
                models_from_pimfile = parse_pimfile(pimfile_path)

            if args.models:
                print(f"Models requested: {args.models}")
                models_from_user_args = parse_models_list(args.models)

            # TODO decide if we want to combine models into one dict -> Initial thought no if dependencies arent provided in cli but can be in Pimfile
            if args.isolated:
                logging.info("Using new isolated environments for all models provided")

            # if not conda_env_exists(env_name):
            #     create_conda_env(env_name, python_version)
            # activate_conda_env(env_name)
            # install_dependencies(env_name, model_deps)
            # conda run -n $env_name pip install ...

        except Exception as e:
            logging.error(e)
            return 1
