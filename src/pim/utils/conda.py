import os
import re
import subprocess
import sys

from pim.cli_utils.printing import warning
from pim.config.config import DEFAULT_PYTHON_VERSION


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


def check_dependency_conflicts(conda_deps, pip_deps):
    """
    Checks for two types of dependency conflicts and logs warnings.
    1. Packages specified for installation by both conda and pip.
    2. Packages specified with multiple different versions across all dependencies.
    """
    # 1. Check for packages present in both conda and pip lists.
    conda_dep_names = {split_dep_first_version(dep)[0] for dep in conda_deps}
    pip_dep_names = {split_dep_first_version(dep)[0] for dep in pip_deps}

    shared_deps = conda_dep_names.intersection(pip_dep_names)
    if shared_deps:
        warning(
            f"The following packages are specified as both conda and pip "
            f"dependencies, which may lead to conflicts: {', '.join(sorted(list(shared_deps)))}"
        )

    # 2. Check for packages with multiple different versions specified.
    all_deps = conda_deps + pip_deps
    parsed_versions = {}
    for dep_str in all_deps:
        name, version = split_dep_first_version(dep_str)
        parsed_versions.setdefault(name, set()).add(version or "unversioned")

    version_conflicts = {
        name: versions
        for name, versions in parsed_versions.items()
        if len(versions) > 1
    }

    if version_conflicts:
        conflict_messages = [
            f"{name} (versions: {', '.join(sorted(list(versions)))})"
            for name, versions in version_conflicts.items()
        ]
        warning(
            f"The following packages have multiple different versions specified, "
            f"which may cause installation issues: {'; '.join(conflict_messages)}"
        )


def split_dep_first_version(dep):
    """
    Split a dependency string into (package name, first version number only).
    Strips specifiers like '==', '>=', etc. If no version is found, returns '' for version.

    Returns:
        (package_name, version)
    """
    spec_pattern = r"(==|>=|<=|!=|>|<|=)"
    match = re.search(spec_pattern, dep)

    if not match:
        return dep.strip(), ""

    name = dep[: match.start()].strip()
    version_part = dep[match.start() :].strip()
    version = re.sub(spec_pattern, "", version_part.split(",")[0]).strip()
    return name, version
