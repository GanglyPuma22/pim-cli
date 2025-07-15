import yaml
from pathlib import Path
import logging

SUPPORTED_FRAMEWORKS = {"huggingface", "torchvision", "sklearn"}


def parse_pimfile(pimfile_path):
    pimfile = Path(pimfile_path)

    if not pimfile.exists():
        raise FileNotFoundError(f"Pimfile not found at {pimfile.resolve()}")

    with open(pimfile, "r") as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict):
        raise ValueError("Pimfile must be a YAML mapping (framework -> list of models)")

    parsed = {}
    for framework, models in data.items():
        if framework not in SUPPORTED_FRAMEWORKS:
            logging.warning(f"Skipping unsupported framework: {framework}")
            continue

        if not isinstance(models, list):
            raise ValueError(f"Expected list of models under '{framework}'")

        parsed[framework] = models

    return parsed


def parse_models_list(models_list):
    """
    This function is used to parse a list of models from the Pimfile.
    It expects a list of strings, where each string can be in the format "framework:model_name"
    If no framework is specified, it defaults to "huggingface".
    """
    if not isinstance(models_list, list):
        raise ValueError("Models list must be a YAML list")

    parsed = {}
    for model in models_list:
        if not isinstance(model, str):
            raise ValueError(f"Model name must be a string: {model}")

        framework, model_name = (
            model.split(":", 1) if ":" in model else ("huggingface", model)
        )
        if framework not in SUPPORTED_FRAMEWORKS:
            logging.warning(f"Skipping unsupported framework: {framework}")
            continue

        if framework not in parsed:
            parsed[framework] = []
        parsed[framework].append(model_name.strip())

    return parsed
