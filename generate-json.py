# This is a sample Python script.
import json


from scrap.allegrolokalnie import AllegroLokalniePage
from scrap.olx.OlxScrapper import OlxScrapper




al_url = "https://allegrolokalnie.pl/oferty/q/krokodyl?sort=startingTime-desc&page=2&zrodlo=lokalnie&zrodlo=allegro"
olx_url = "https://www.olx.pl/dla-dzieci/zabawki/maskotki/q-krokodyl/?search%5Border%5D=created_at:desc&page=1"

al = AllegroLokalniePage.fetch(al_url)
al_ads = al.to_dict()

scrapper = OlxScrapper(debug=False)
result = scrapper.scrap_all_pages(olx_url)
olx_ads = result.get_all_raw_ads()
result = {
    "olx_ads": olx_ads,
    "al_ads": al_ads
}
print(json.dumps(result))
