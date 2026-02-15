from urllib.parse import urlparse, parse_qs, urlencode
import requests
from scrap.cache import Cache
from scrap.olx.ScriptRegex import ScriptRegex


class OlxLink:
    def __init__(self, url: str):
        self.url = url
        url_parts = urlparse(url)
        self.valid = url_parts.netloc == "www.olx.pl" or url_parts.netloc == "olx.pl"
        self.base_url = url_parts.scheme + "://" + url_parts.netloc
        self.path = url_parts.path
        self.query = url_parts.query
        query_params = parse_qs(self.query)
        self.full_url = self.base_url + self.path + "?" + self.query
        new_query_params = {}
        for item, v in query_params.items():
            new_query_params[item] = v[0] if len(v) == 1 else v
        self.query_params = new_query_params

    @staticmethod
    def get_single_value(v):
        return v[0] if isinstance(v, list) and len(v) else v
    def get_url(self) -> str:
        return self.url
    def get_full_url(self) -> str:
        return self.full_url
    def get_query_params(self) -> dict:
        return self.query_params
    def get_page_number(self) -> int:
        if "page" in self.query_params:
            return int(self.get_single_value(self.query_params["page"]))
        return 1
    def get_next_page_url(self) -> str:
        url = self.base_url + self.path
        qp = self.query_params
        qp["page"] = self.get_page_number() + 1
        qp_encoded = urlencode(qp)
        if len(qp_encoded) > 0:
            url += "?" + qp_encoded
        return url

    def is_valid(self) -> bool:
        return self.valid

class InvalidOLXLink(Exception):
    pass

class OlxAdParam:
    def __init__(self, param):
        self.__param = param
        self.key = param["key"]
        self.name = param["name"]
        self.type = param["type"]
        self.value = param["value"]
        self.normalized_value = param["normalizedValue"]

class OlxAdParams:
    def __init__(self, params):
        self.params = params
    def count(self):
        return len(self.params)
    def get_param(self, index: int):
        return self.params[index]
    def get_param_by_key(self, key):
        for param in self.params:
            if param["key"].lower() == key.lower():
                return param
        return None
    def get_param_by_name(self, name : str):
        for param in self.params:
            if param["name"].lower() == name.lower():
                return param
        return None

class OlxAdPrice:
    def __init__(self, price):
        self.__price = price
    def __get_regular_price_prop(self, prop, default = None):
        p = self.__price
        if "regularPrice" in p and prop in p["regularPrice"]:
            return p["regularPrice"][prop]
        return default
    def get_value(self):
        return self.__get_regular_price_prop("value", default=0.00)
    def get_currency_code(self):
        return self.__get_regular_price_prop("currencyCode")
    def get_currency_symbol(self):
        return self.__get_regular_price_prop("currencySymbol")
    def get_full_price(self):
        return self.get_value() + " " + self.get_currency_symbol()

class OlxAdLocation:
    def __init__(self, location):
        self._location = location
    def get_city_name(self):
        return self._location["cityName"]
    def get_city_id(self):
        return self._location["cityId"]
    def get_city_normalized_name(self):
        return self._location["cityNormalizedName"]
    def get_region_name(self):
        return self._location["regionName"]
    def get_region_id(self):
        return self._location["regionId"]
    def get_region_normalized_name(self):
        return self._location["regionNormalizedName"]
    def get_district_name(self):
        return self._location["districtName"]
    def get_district_id(self):
        return self._location["districtId"]
    def get_path_name(self):
        return self._location["pathName"]

class OlxAd:
    def __init__(self, ad: dict):
        self.ad = ad

    def get_id(self):
        return self.ad["id"]

    def get_title(self):
        return self.ad["title"]
    def get_description(self):
        return self.ad["description"]
    def get_url(self):
        return self.ad["url"]
    def get_map(self):
        return self.ad["map"]
    def get_category(self):
        return self.ad["category"]
    def get_created_time(self):
        return self.ad["created_time"]
    def get_last_refresh_time(self):
        return self.ad["last_refresh_time"]
    def get_valid_to_time(self):
        return self.ad["valid_to_time"]
    def is_active(self):
        return self.ad["isActive"]
    def get_status(self):
        return self.ad["status"]
    def get_params(self):
        return OlxAdParams(self.ad["params"])
    def get_item_condition(self):
        return self.ad["itemCondition"]
    def get_price(self):
        return OlxAdPrice(self.ad["price"])
    def get_photos(self):
        return self.ad["photos"]
    def get_photos_set(self):
        return self.ad["photosSet"]
    def get_location(self):
        return OlxAdLocation(self.ad["location"])


class OlxAdsCollection:
    def __init__(self, ads):
        self.ads = ads

    def count(self):
        return len(self.ads)

    def get_ad(self, index):
        return OlxAd(self.ads[index])

class OlxScrapResult:
    def __init__(self, data: dict):
        self.PRERENDERED_STATE = data["PRERENDERED_STATE"]
        self.PAGE_TRANSLATIONS = data["PAGE_TRANSLATIONS"]
        self.SELECTED_LANGUAGE_ISO_CODE = data["SELECTED_LANGUAGE_ISO_CODE"]

    def get_listing(self):
        return self.PRERENDERED_STATE["listing"]["listing"]

    def get_page_number(self) -> int:
        return self.get_listing()["pageNumber"]
    def get_total_elements(self):
        return self.get_listing()["totalElements"]
    def get_visible_elements(self):
        return self.get_listing()["visibleElements"]
    def get_total_pages(self):
        return self.get_listing()["totalPages"]
    def get_ads(self):
        return self.get_listing()["ads"]



class OlxScrapper:

    def __init__(self, debug = False):
        self.debug = debug

    def scrap(self, url: str):
        link = OlxLink(url)
        print(link.get_page_number())
        print(link.get_next_page_url())
        if not link.is_valid():
            raise InvalidOLXLink("Invalid URL")
        cache = Cache()

        if cache.is_url_cached(url):
            resp = cache.read_cache(url)
        else:
            resp = requests.get(url).text
            cache.write_cache(url, resp)
        if self.debug:
            print(resp)
        r = ScriptRegex()
        c = r.find_olx_data(resp)
        return OlxScrapResult(c)

