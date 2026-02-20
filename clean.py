import pathlib
from helpers.file.CacheCleaner import CacheCleaner
import os

current_path = pathlib.Path().resolve()
cache_path = os.path.join(current_path, 'cache')

cleaner = CacheCleaner(deprecation_seconds=60*15)
cleaner.clean_deprecated_files(cache_dir=cache_path)
