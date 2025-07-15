from pathlib import Path
import os

# Default: ~/.cache/pim
DEFAULT_CACHE_DIR = Path(os.getenv("PIM_CACHE_DIR", "~/.cache/pim")).expanduser()

# Base conda env name (for shared use)
DEFAULT_CONDA_ENV_NAME = "pim-ai"

# Default Python version for new envs
DEFAULT_PYTHON_VERSION = "3.11"

# Prefix for isolated environments
ISOLATED_ENV_PREFIX = "pim-isolated"

# # Location of registry or Pimfile fallback
# DEFAULT_PIMFILE = Path.cwd() / "Pimfile"
