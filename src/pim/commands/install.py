from pim.config.config import DEFAULT_CONDA_ENV_NAME, DEFAULT_PYTHON_VERSION
from pim.commands.base import BaseCommand
from pim.utils.conda import (
    conda_env_exists,
    create_conda_env,
    install_dependencies_in_env,
)
from pim.commands.utils.parsing import (
    combine_parsed_dicts,
    parse_models_list,
    parse_pimfile,
)
from pim.commands.utils.installers import install_models
from pim.utils.pathing import find_pimfile, validate_cache_path, validate_file_path
from pim.cli_utils.printing import info, debug, success, warning, handle_cli_error


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
            action="store_true",
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
            model_data_from_pimfile = None
            model_data_from_user_args = None
            # Check if models list is empty
            if not args.models or args.file:
                pimfile_path = (
                    find_pimfile()
                    if args.file is None
                    else validate_file_path(args.file)
                )
                info(
                    f"Installing models and dependencies from {pimfile_path} and saving to {cache_dir}",
                    style="bold blue",
                )
                # TODO Update parser to handle dependencies too and python version
                model_data_from_pimfile = parse_pimfile(pimfile_path)

            if args.models:
                debug(f"Models requested at CLI: {args.models}")
                model_data_from_user_args = parse_models_list(args.models)

            # TODO Document struct more clearly
            # Combine models into one dict
            combined_model_data = combine_parsed_dicts(
                model_data_from_pimfile, model_data_from_user_args
            )

            # TODO decide if we want to combine models into one dict -> Initial thought no if dependencies arent provided in cli but can be in Pimfile
            if args.isolated:
                info(
                    "Using new isolated environments for all models provided!",
                    style="bold yellow",
                )
                # TODO Handle isolated environments
            else:
                base_conda_env_name = DEFAULT_CONDA_ENV_NAME
                if "env-name" in combined_model_data:
                    base_conda_env_name = combined_model_data["env-name"]

                info(
                    f"Using {base_conda_env_name} conda environment for all models provided, this will install all dependencies in the same environment"
                )

                # Check if base conda env doesnt already exist
                if conda_env_exists(base_conda_env_name):
                    warning(
                        f"{base_conda_env_name} conda environment already exists, skipping creation."
                    )
                else:
                    info(
                        f"Creating new conda environment: {base_conda_env_name} with Python {DEFAULT_PYTHON_VERSION}",
                        style="bold blue",
                    )
                    # Create the base conda environment
                    create_conda_env(base_conda_env_name)
                    success(f"Conda environment created: {base_conda_env_name}")

                install_dependencies_in_env(
                    base_conda_env_name,
                    combined_model_data.get("conda-dependencies", None),
                    combined_model_data.get("pip-dependencies", None),
                )

                install_models(combined_model_data, cache_dir, args.auth)
                # for framework, model_data in combined_model_data.items():

            # # Install models and dependencies
            # for framework, models in model_data_from_pimfile.items():
            #     for model in models:
            #         if framework == "huggingface":
            #             install_huggingface(model, cache_dir, use_auth=args.auth)
            #         elif framework == "torchvision":
            #             install_torchvision(model, cache_dir)
            #         elif framework == "sklearn":
            #             # Pass the project root to resolve the relative path
            #             install_sklearn(model, cache_dir)
            #         else:
            #            logger.warning(f"Unsupported framework: {framework}")

        except Exception as e:
            handle_cli_error(e)
