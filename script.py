# This is a sample Python script.
import json

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from helpers.uri import get_uri_params
from scrap.allegrolokalnie import AllegroLokalniePage, AllegroLokalnieItem
import sys
from helpers.file.fileinfo import FileInfo, FileDeprecation
from gui.MainWindowV2 import MainWindow, main
from scrap.olx.OlxScrapper import OlxScrapper


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("Fetch allegrolokalnie.pl")
    al_url = "https://allegrolokalnie.pl/oferty/q/krokodyl?sort=startingTime-desc&page=2&zrodlo=lokalnie&zrodlo=allegro"
    print("Fetch olx.pl")
    olx_url = "https://www.olx.pl/dla-dzieci/zabawki/maskotki/q-krokodyl/?search%5Border%5D=created_at:desc&page=1"
    destination_path = "C:\\Users\\test\\Documents\\electron\\crawler-app\\src\\data"
    destination_al_file = destination_path  + '\\allegrolokalnie.json'
    destination_olx_file = destination_path + '\\olx.json'

    al = AllegroLokalniePage.fetch(al_url)
    with open(destination_al_file, 'w', encoding="utf-8") as fp:
        json.dump(al.to_dict(), fp, indent=4)
    print("AllegroLokalnie.pl data saved in {}".format(destination_al_file))

    scrapper = OlxScrapper(debug=False)
    result = scrapper.scrap_all_pages(olx_url)
    with open(destination_olx_file, 'w', encoding="utf-8") as fp:
        json.dump(result.get_all_raw_ads(), fp, indent=4)
    print("Olx.pl data saved in {}".format(destination_olx_file))

    #
    # for crocodile in items:
    #      print(crocodile.get_title())
    #      print(crocodile.get_price() + crocodile.get_price_currency())
    #      print(crocodile.get_link())
    #      print(crocodile.get_image())
    # print(pages, page)
    sys.exit()


    url = "https://www.olx.pl/dla-dzieci/zabawki/maskotki/q-krokodyl/?search%5Border%5D=created_at:desc&page=1"
    scrapper = OlxScrapper(debug=False)
    result = scrapper.scrap_all_pages(url)
    all_ads = result.get_all_ads()
    for ad in all_ads:
        print(ad.get_title())

    print("*" * 32)
    print("All ads count: {}".format(len(all_ads)))
    print("*" * 32)
    with open('olx_ads.json', 'w', encoding="utf-8") as f:
        json.dump(result.get_all_raw_ads(), f, ensure_ascii=False, indent=4)

    #print(sr.PRERENDERED_STATE["listing"]["listing"])
    #print(sr.get_page_number())
    #with open('prerendered_data.json', 'w', encoding="utf-8") as f:
    #    json.dump(sr.PRERENDERED_STATE["listing"]["listing"], f, indent=4)
    #    #json.dump(sr.PRERENDERED_STATE, sys.stdout, indent=4)

    sys.exit()

    cache_file = "cache/bc3c23aaf5319a0c83c4bacadc06665e"
    fi = FileInfo(cache_file)
    if fi.does_file_exist():
        print(fi.how_long_exists()/60/60)

    fd = FileDeprecation()
    fd.clean_directory_from_deprecated_files("cache")



    al = AllegroLokalniePage.fetch("https://allegrolokalnie.pl/oferty/q/krokodyl?sort=startingTime-desc&page=2&zrodlo=lokalnie&zrodlo=allegro")
    items = al.get_items()
    pages = al.get_pages_count()
    page = al.get_pages_index()
    #print(pages, page)

    # for crocodile in items:
    #     print(crocodile.get_title())
    #     print(crocodile.get_price() + crocodile.get_price_currency())
    #     print(crocodile.get_link())
    #     print(crocodile.get_image())

    main(items)




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
