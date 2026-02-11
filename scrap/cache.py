import os
from helpers.md5 import md5_string_hash

class Cache:
    def __init__(self):
        self.directory = "cache"
    def is_url_cached(self, url):
        hash_string = md5_string_hash(url)
        return os.path.exists(os.path.join(self.directory, hash_string))
    def write_cache(self, url, content):
        hash_string = md5_string_hash(url)
        open(os.path.join(self.directory, hash_string), 'w').write(content)
    def read_cache(self, url):
        if not self.is_url_cached(url):
            return None
        hash_string = md5_string_hash(url)
        return open(os.path.join(self.directory, hash_string), 'r').read()
    def remove_cache(self, url):
        hash_string = md5_string_hash(url)
        if self.is_url_cached(url):
            os.remove(os.path.join(self.directory, hash_string))
            return True
        return False