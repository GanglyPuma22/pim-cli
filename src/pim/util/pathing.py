import os
from pathlib import Path

def get_cache_dir():
    cache_dir_path = Path(os.environ.get("PIM_CACHE_DIR", "~/.cache/pim")).expanduser()
    cache_dir_path.mkdir(parents=True, exist_ok=True)
    return cache_dir_path.resolve()

def find_pimfile(start_path=Path.cwd()):
    for path in [*start_path.parents, start_path]:
        pimfile = path / "Pimfile"
        if pimfile.exists():
            return pimfile
    raise FileNotFoundError("No Pimfile found in current directory or any parent directories.")