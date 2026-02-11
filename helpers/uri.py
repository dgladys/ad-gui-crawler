import json
import validators
from urllib.parse import urlparse, parse_qs

def get_uri_params(url):
    parsed = urlparse(url)
    qs = parse_qs(parsed.query)
    result = {}
    for k, v in qs.items():
        if len(v)==1:
            v = v[0]
        result[k] = v
    return result

class UriParams:
    def __init__(self, url):
        self.url = url
        self.valid = False if not validators.url(url) else True
        self.params = get_uri_params(url) if self.is_valid else {}

    def get_params(self):
        return self.params

    def get_param(self, param, default=None):
        return self.params[param] if param in self.params else default

    def get_int(self, param, default=None):
        return int(self.params[param]) if param in self.params else default

    def count(self):
        return len(self.params)

    def has_param(self, param):
        return param in self.params

    def to_json(self):
        return json.dumps(self.params)

    def get_url(self):
        return self.url

    def is_valid(self):
        return self.valid