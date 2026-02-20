
import os

from helpers.file.fileinfo import FileDeprecation


class CacheCleaner:
    def __init__(self, deprecation_seconds):
        self.deprecation_seconds = deprecation_seconds

    def get_deprecated_files(self, cache_dir = "cache"):
        deprecation = FileDeprecation(deprecation_seconds=self.deprecation_seconds)
        all_cache_files = self._get_all_cache_files(cache_dir=cache_dir)
        deprecated_files = []
        for file in all_cache_files:
            if deprecation.is_deprecated(file["filepath"]):
                deprecated_files.append(file)
        return deprecated_files

    def clean_deprecated_files(self, cache_dir = "cache"):
        deprecated_files = self.get_deprecated_files(cache_dir=cache_dir)
        deprecation = FileDeprecation(deprecation_seconds=self.deprecation_seconds)
        for file in deprecated_files:
            print("\t{} Remove deprecated".format(file["filepath"]))
            deprecation.remove_file_if_deprecated(file["filepath"])


    def _get_all_cache_files(self, cache_dir: str):
        all_cache_files = []
        for cache_file in os.listdir(cache_dir):
            if len(cache_file) == 32:
                all_cache_files.append({
                    "filename": cache_file,
                    "filepath": os.path.join(cache_dir, cache_file)
                })
        return all_cache_files