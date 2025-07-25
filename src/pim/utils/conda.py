import os
import subprocess
import sys

from pim.config.settings import DEFAULT_PYTHON_VERSION


def conda_env_exists(env_name):
    conda_info = subprocess.run(
        ["conda", "info", "--base"], capture_output=True, text=True
    )
    base_path = conda_info.stdout.strip().splitlines()[-1]
    return os.path.exists(os.path.join(base_path, "envs", env_name))


def install_dependencies_in_env(env_name, conda_deps, pip_deps):
    """
    Install conda and pip dependencies in the specified conda environment.
    """
    if conda_deps:
        subprocess.run(
            ["conda", "run", "-n", env_name, "conda", "install", "-y"] + conda_deps,
            check=True,
            stdout=sys.stdout,
            stderr=sys.stderr,
        )

    if pip_deps:
        subprocess.run(
            ["conda", "run", "-n", env_name, "pip", "install"] + pip_deps,
            check=True,
            stdout=sys.stdout,
            stderr=sys.stderr,
        )


def create_conda_env(base_conda_env_name):
    """
    Create a new conda environment with the specified name and Python version.
    """
    subprocess.run(
        [
            "conda",
            "create",
            "-n",
            base_conda_env_name,
            f"python={DEFAULT_PYTHON_VERSION}",
            "-y",
            "-q",
        ],
        check=True,
    )


def has_rejected_tos():
    try:
        result = subprocess.run(
            ["conda", "info", "--json"], capture_output=True, text=True, check=True
        )
        return "pkgs/main" in result.stdout and "tos" in result.stdout
    except:
        return False
