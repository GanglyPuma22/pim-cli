import os
from pathlib import Path

from pim.config.settings import DEFAULT_CACHE_DIR


# TODO Use conf variable for default cache path
def validate_cache_path(string_path):
    """
    This function is used to validate the cache directory path.
    It ensures the directory exists and resolves the full path.
    If the directory is not specified, it defaults to the environment variable PIM_CACHE_DIR, and if that is not set it uses the default path ~/.cache/pim
    """
    cache_dir_path = Path(string_path) if string_path else DEFAULT_CACHE_DIR
    cache_dir_path.mkdir(parents=True, exist_ok=True)
    return cache_dir_path.resolve()


def find_pimfile(start_path=Path.cwd()):
    """
    This function is used to find the Pimfile in the current directory or any parent directories.
    It returns the path to the Pimfile if found, otherwise raises a FileNotFoundError.
    """
    for path in [*start_path.parents, start_path]:
        pimfile = path / "Pimfile"
        if pimfile.exists():
            return pimfile
    raise FileNotFoundError(
        "No Pimfile found in current directory or any parent directories."
    )


def validate_file_path(string_path):
    """
    This function is used to validate a file path.
    It checks if the file exists and is a regular file (not a directory), returning its absolute path.
    """
    path = Path(string_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    if not path.is_file():
        raise IsADirectoryError(f"Path is a directory not a file: {path}")
    return path.resolve()
