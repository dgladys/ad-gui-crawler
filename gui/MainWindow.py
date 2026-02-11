import urllib

from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt, pyqtSignal, QItemSelection
from PyQt6.QtGui import QStandardItemModel, QPixmap, QIcon
from PyQt6.QtWidgets import QMainWindow, QPushButton, QApplication, QTreeView, QSplitter
from PyQt6.QtGui import QStandardItem

from gui.Image import ImageFactory
from scrap.allegrolokalnie import AllegroLokalnieItem


class TreeViewModelItem(QStandardItem):
    def __init__(self, name, ad_item = None, /, *__args):
        self.ad_item = ad_item
        super().__init__(name, *__args)

    def get_ad_item(self):
        return self.ad_item

class AdDetails(QSplitter):

    def __init__(self):
        super().__init__()
        self.setOrientation(Qt.Orientation.Horizontal)

        self.image = ImageFactory.create_from_url('https://a.allegroimg.com/s180x180/1199be/f7e42f93403f8b2c76076c04235f')
        self.image.#resize(320, 240)
        self.addWidget(self.image)



def create_allegrolokalnie_tree_view(items: list[AllegroLokalnieItem], details: AdDetails) -> QTreeView:
    tree = QTreeView()

    model = QStandardItemModel()
    model.setHorizontalHeaderLabels(['Name', 'Price', 'State', 'Address'])

    parent = TreeViewModelItem('Allegro Lokalnie')
    model.appendRow([parent, TreeViewModelItem('')])

    items = list(items)
    items.sort(key=AllegroLokalnieItem.get_sort_lambda())

    def on_item_select(item: QItemSelection):
        selected_indices = tree.selectionModel().selectedIndexes()
        items = [model.itemFromIndex(index) for index in selected_indices]
        selectedCroco = items[0]
        """ param (scrap.allegrolokalnie.AllegroLokalnieItem): ad """
        ad: AllegroLokalnieItem = selectedCroco.get_ad_item()
        if ad is not None and ad.get_image():
            print(ad.get_image())
            details.image.load_from_url(ad.get_image())



        #selection = item.indexes()[0]
        #print(selection.row(), selection.column(), selection.data(), selection.)
        # r = selection.row()
        # c = selection.column()
        # p = selection.parent()
        # print(r)
        # print(c)
        # print(model.item(0, 0).model().item(r, c))


    for item in items:

        state = item.get_product_state()
        parent.appendRow([
            TreeViewModelItem(item.get_title(), item),
            TreeViewModelItem(item.get_price() + " " + item.get_price_currency()),
            TreeViewModelItem(state if state else "-"),
            TreeViewModelItem(item.get_address())
        ])


    # 3. Konfigurujemy QTreeView

    tree.setModel(model)
    tree.expandAll()
    tree.resizeColumnToContents(0)

    """ param (PyQt6.QtCore.pyqtSignal): Signal selection changed """
    signal = tree.selectionModel().selectionChanged
    #signal = tree.selectionModel().ite
    signal.connect(on_item_select)

    return tree




class MainWindow(QMainWindow):
    def __init__(self, items: list[AllegroLokalnieItem]):
        super().__init__()
        self.setWindowTitle("Hello, World!")
        self.resize(800, 600)
        self.ad_details = AdDetails()
        tree_view = create_allegrolokalnie_tree_view(items, self.ad_details)
        splitter = QSplitter()
        splitter.setOrientation(Qt.Orientation.Vertical)
        splitter.addWidget(tree_view)

        splitter.addWidget(self.ad_details)

        self.setCentralWidget(splitter)

        self.show()


def main(items: list[AllegroLokalnieItem]):
    app = QApplication([])
    window = MainWindow(items)
    app.exec()