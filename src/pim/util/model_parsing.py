import yaml
from pathlib import Path
from pim.config.settings import DEFAULT_CONDA_ENV_NAME, SUPPORTED_FRAMEWORKS
import logging


def initialize_parsed_dict():
    """
    Initialize a dictionary to hold parsed Pimfile data.
    It contains the supported frameworks as keys with empty lists
    """
    parsed = {}
    for framework in SUPPORTED_FRAMEWORKS:
        parsed[framework] = []
    return parsed


def combine_parsed_dicts(dict1, dict2):
    """
    Combine two parsed dictionaries, merging lists for each framework.
    If a framework exists in both, their lists are concatenated.
    """
    if dict2 is None:
        return dict1
    if dict1 is None:
        return dict2

    combined = initialize_parsed_dict()
    for framework in SUPPORTED_FRAMEWORKS:
        combined[framework] = dict1.get(framework, []) + dict2.get(framework, [])

    # Carry over any additional keys
    for dict in [dict1, dict2]:
        for key in dict.keys():
            # Be careful, this assumes both dicts do not have conflicting keys outside of the supported frameworks
            if key not in combined:
                combined[key] = dict[key]

    return combined


def parse_pimfile(pimfile_path):
    pimfile = Path(pimfile_path)

    if not pimfile.exists():
        raise FileNotFoundError(f"Pimfile not found at {pimfile.resolve()}")
    try:
        with open(pimfile, "r") as f:
            data = yaml.safe_load(f)

            if not isinstance(data, dict):
                raise ValueError(
                    "Pimfile must be a YAML mapping (framework -> list of models)"
                )

            env_name = data.pop("env-name", DEFAULT_CONDA_ENV_NAME)
            if env_name in SUPPORTED_FRAMEWORKS:
                raise ValueError(
                    f"Environment name '{env_name}' conflicts with supported framework names. Please choose a different name."
                )

            parsed = initialize_parsed_dict()
            parsed["env-name"] = env_name
            conda_depencies = []
            pip_dependencies = []

            for framework, model_data in data.items():
                if framework not in SUPPORTED_FRAMEWORKS:
                    logging.warning(f"Skipping unsupported framework: {framework}")
                    continue

                for model in model_data:
                    # Save model name to parsed dict to install at once
                    parsed[framework].append(model["name"])

                    # TODO Handle case where no deps (Not required in pimfile)
                    if "dependencies" in model:
                        # Gather dependencies into conda and pip lists
                        for dep in model["dependencies"]:
                            # Currently we only support conda and pip dependencies, so if its a dict it has to be pip
                            if isinstance(dep, dict):
                                # Handle pip dependencies
                                if "pip" in dep:
                                    pip_dependencies.extend(dep["pip"])
                            else:
                                conda_depencies.append(dep)

            parsed["conda-dependencies"] = conda_depencies
            parsed["pip-dependencies"] = pip_dependencies
            return parsed
    except Exception as e:
        logging.error(f"Error parsing Pimfile: {e}")
        raise ValueError(f"Invalid Pimfile format: {e}")


def parse_models_list(models_list):
    """
    This function is used to parse a list of models from the Pimfile.
    It expects a list of strings, where each string can be in the format "framework:model_name"
    If no framework is specified, it defaults to "huggingface".
    """
    if not isinstance(models_list, list):
        raise ValueError("Models list must be a YAML list")

    parsed = initialize_parsed_dict()
    for model in models_list:
        if not isinstance(model, str):
            raise ValueError(f"Model name must be a string: {model}")

        framework, model_name = (
            model.split(":", 1) if ":" in model else ("huggingface", model)
        )
        if framework not in SUPPORTED_FRAMEWORKS:
            logging.warning(f"Skipping unsupported framework: {framework}")
            continue

        parsed[framework].append(model_name.strip())

    return parsed
