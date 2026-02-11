# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from helpers.uri import get_uri_params
from scrap.allegrolokalnie import AllegroLokalniePage, AllegroLokalnieItem
import sys
from helpers.file.fileinfo import FileInfo, FileDeprecation
from gui.MainWindow import MainWindow, main

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

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
