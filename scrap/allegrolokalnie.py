from bs4 import BeautifulSoup, Tag
from typing import Self
import sys

from scrap.base_page import BasePage

class AllegroLokalnieItem:
    def __init__(self, item: Tag):
        self.item = item
        self.price = self.get_price_as_int()
        self.address = self.get_address()

    def compare_by_price(self, item: Self):
        return self.price - item.price

    @staticmethod
    def get_sort_lambda():
        return lambda item: -(sys.maxunicode - item.price) if item.address == "Kraków" else item.price

    def get_price_as_int(self):
        try:
            return int(self.get_price())
        except Exception as e:
            print(e)
            return 0

    def get_link(self):
        link = self.item.attrs["href"]
        if link.startswith("/"):
            link = "https://www.allegrolokalnie.pl" + link
        return link
    def get_title(self):
        return self.item.find("h3").text
    def get_price(self):
        return self.item.find("span", {"class": "ml-offer-price__dollars"}).text.replace(" ", "")
    def get_price_currency(self):
        return self.item.find("span", {"class": "ml-offer-price__currency"}).text

    def get_full_price(self) -> str:
        return (self.get_price() + " " + self.get_price_currency()).strip()


    def get_image(self):
        return self.item.find("img")["src"]

    def get_address(self):
        addr = self.item.find('address', {"itemprop" : "address"})
        return addr.text.strip() if addr else ""

    def find_by_class(self, node_type, class_name, parent: Tag = None):
        search_node = self.item if parent is None else parent
        return search_node.find(node_type, {"class": class_name})

    def get_badges(self):
        badges = self.find_by_class("ul", "ml-badges ml-badges mlc-itembox__badges__badge")
        return badges.find_all("li")

    def get_badge_starts_with(self, search_text):
        li_list = self.get_badges()
        for li in li_list:
            li_text = li.text.strip()
            if li_text.startswith(search_text):
                return li_text[len(search_text):].strip()
        return ""
    def get_product_state(self):
        return self.get_badge_starts_with("STAN: ")
        #return self.item.find("ul", {"class": "ml-badges ml-badges mlc-itembox__badges__badge"})

class AllegroLokalniePage(BasePage):

    def __init__(self, url, content):
        super().__init__(url, content)
        self.title = ""
        self.parsed_content = BeautifulSoup(content, "html.parser")
    @staticmethod
    def fetch(url):
        content = BasePage.fetch_content(url)
        return AllegroLokalniePage(url, content)


    def get_title(self):
        return self.parsed_content.find("title").text

    def get_pages_index(self):
        return self.parsed_content.find("input", {"class": "ml-pagination__input"}).attrs["value"]

    def get_pages_count(self):
        pages_count = self.parsed_content.find("span", {"class": "ml-pagination__count"}).text
        if pages_count.startswith("z "):
            pages_count = pages_count[2:]
        return int(pages_count)

    def get_items(self):
        items = self.parsed_content.find_all("a", {"class": "mlc-card mlc-itembox"})
        return map(lambda item: AllegroLokalnieItem(item), items)
