from vinted_scraper import VintedScraper


class VintedScraperService:

    def __init__(self, url):
        self.url = url
        self.scraper = VintedScraper(url)

    def scrap(self, search_text):
        return self.scraper.search({"search_text": search_text})

    @staticmethod
    def init_com(self):
        return VintedScraperService("https://www.vinted.com")
    @staticmethod
    def init_pl(self):
        return VintedScraperService("https://www.vinted.pl")



