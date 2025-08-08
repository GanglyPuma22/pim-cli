import os
import inspect
import torchvision.models as torchvision_models
from pathlib import Path
from pim.cli_utils.printing import warning
from huggingface_hub import snapshot_download


def install_models(model_data, cache_dir=None, auth=None):
    """
    Install models based on the provided model data.
    This function should handle the installation logic for each supported framework.
    """
    if not model_data:
        raise ValueError("No model data provided for installation.")

    for framework, models in model_data.items():
        if framework == "huggingface":
            install_huggingface(models, cache_dir, use_auth=auth)
        elif framework == "torchvision":
            install_torchvision(models, cache_dir)
        elif framework == "sklearn":
            install_sklearn(models, cache_dir)
        elif framework == "custom":
            install_custom(models, cache_dir)
        else:
            warning(f"Unsupported framework: {framework}")


def install_sklearn(models, cache_dir=None):
    """
    Install scikit-learn models.
    """
    return


def install_custom(models, cache_dir=None):
    """
    Install custom models.
    """
    return


def install_torchvision(models, cache_dir=None):
    """
    Install torchvision models.
    """
    return


def install_huggingface(models, cache_dir=None, use_auth=None):
    """
    Install Hugging Face models.
    """
    # TODO Handle auth
    for model in models:
        snapshot_download(model["name"])


def get_torchvision_model(name, pretrained=True, cache_dir=None):
    """
    Load a torchvision model with optional pretrained weights and a custom cache directory.

    Args:
        name (str): Model name from torchvision.models
        pretrained (bool): Whether to load pretrained weights
        cache_dir (str | Path): Optional custom directory to use for model weight caching

    Returns:
        model (torch.nn.Module): The loaded model
        preprocess (Callable | None): The transform associated with the weights
    """
    if cache_dir:
        os.environ["TORCH_HOME"] = str(Path(cache_dir).resolve())

    try:
        model_fn = getattr(torchvision_models, name)
    except AttributeError:
        raise ValueError(f"Model '{name}' not found in torchvision.models")

    # Handle new Weights API (PEP-style enums)
    if hasattr(model_fn, "__annotations__") and "weights" in model_fn.__annotations__:
        weights_enum = model_fn.__annotations__["weights"]
        weights = weights_enum.DEFAULT if pretrained else None
        model = model_fn(weights=weights)
        preprocess = weights.transforms() if weights else None
    else:
        # Legacy API
        model = model_fn(pretrained=pretrained)
        preprocess = None

    return model, preprocess


def list_torchvision_models():
    """
    List all available torchvision models.
    """
    return [
        name
        for name in dir(torchvision_models)
        if callable(getattr(torchvision_models, name)) and not name.startswith("_")
    ]


def get_available_weights(model_name: str):
    try:
        model_fn = getattr(torchvision_models, model_name)
    except AttributeError:
        raise ValueError(f"No model named '{model_name}' in torchvision.models")

    # Skip if it's not callable (i.e., not a model function)
    if not callable(model_fn):
        raise TypeError(f"'{model_name}' is not a callable model constructor")

    # Try to find the associated Weights enum class
    for attr_name in dir(torchvision_models):
        attr = getattr(torchvision_models, attr_name)
        if inspect.isclass(attr) and attr_name.lower().startswith(model_name.lower()):
            if hasattr(attr, "__members__"):  # looks like an Enum
                return list(attr.__members__.keys())

    # Fallback: no Weights enum found
    return []


# def get_available_weights(model_name):
#     try:
#         model_fn = getattr(models, model_name)
#     except AttributeError:
#         raise ValueError(f"No model named '{model_name}' found in torchvision.models")

#     # Check if the model uses the Weights Enum pattern
#     annotations = getattr(model_fn, "__annotations__", {})
#     if "weights" not in annotations:
#         return []

#     weights_enum = annotations["weights"]
#     return list(weights_enum.__members__.keys())
