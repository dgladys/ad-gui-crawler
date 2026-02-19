import os
from helpers.md5 import md5_string_hash

class CacheUnreadableException(Exception):
    pass

class Cache:
    def __init__(self):
        self.directory = "cache"
    def is_url_cached(self, url):
        hash_string = md5_string_hash(url)
        return os.path.exists(os.path.join(self.directory, hash_string))
    def write_cache(self, url, content):
        hash_string = md5_string_hash(url)
        open(os.path.join(self.directory, hash_string), 'w', encoding="utf-8").write(content)
    def read_cache(self, url):
        if not self.is_url_cached(url):
            return None
        hash_string = md5_string_hash(url)
        cache_file_path = os.path.join(self.directory, hash_string)
        try:
            return open(cache_file_path, 'r', encoding="utf-8").read()
        except Exception as e:
            raise CacheUnreadableException("Cannot read cache file: {}".format(cache_file_path)) from e

    def remove_cache(self, url):
        hash_string = md5_string_hash(url)
        if self.is_url_cached(url):
            os.remove(os.path.join(self.directory, hash_string))
            return True
        return False