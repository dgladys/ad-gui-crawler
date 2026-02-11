from scrap.cache import Cache
import requests

def get_page(url):
    content = requests.get(url)
    return content.text

class BasePage:
    def __init__(self, url, content):
        self.url = url
        self.content = content

    @staticmethod
    def fetch_content(url):
        cache = Cache()
        if cache.is_url_cached(url):
            content = cache.read_cache(url)
        else:
            content = get_page(url)
            cache.write_cache(url, content)
        return content

    def get_content(self):
        return self.content

    def get_url(self):
        return self.url
