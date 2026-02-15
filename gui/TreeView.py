from PyQt6.QtGui import QStandardItem
from PyQt6.QtGui import QStandardItemModel
from PyQt6.QtWidgets import QTreeView
from gui.AdDetail import AdDetails
from scrap.allegrolokalnie import AllegroLokalnieItem


class TreeViewModelItem(QStandardItem):
    def __init__(self, name, ad_item = None, /, *__args):
        self.ad_item = ad_item
        super().__init__(name, *__args)

    def get_ad_item(self):
        return self.ad_item


class AdTreeView(QTreeView):
    def __init__(self, items=None, parent=None, details: AdDetails = None):
        super().__init__(parent)
        if items is None:
            items = []
        self.items = items
        self.model = QStandardItemModel()
        self.init_model()
        self.init_tree_view()
        self.details = details

    def init_model(self):
        self.model.setHorizontalHeaderLabels(['Name', 'Price', 'State', 'Address'])
        parent = TreeViewModelItem('Allegro Lokalnie')
        items = list(self.items)
        items.sort(key=AllegroLokalnieItem.get_sort_lambda())
        for item in items:
            state = item.get_product_state()
            parent.appendRow([
                TreeViewModelItem(item.get_title(), item),
                TreeViewModelItem(item.get_price() + " " + item.get_price_currency()),
                TreeViewModelItem(state if state else "-"),
                TreeViewModelItem(item.get_address())
            ])
        self.model.appendRow([parent, TreeViewModelItem('')])


    def init_tree_view(self):
        self.setModel(self.model)
        self.expandAll()
        self.resizeColumnToContents(0)
        signal = self.selectionModel().selectionChanged
        signal.connect(self.on_item_select)

    def on_item_select(self):
        selected_indices = self.selectionModel().selectedIndexes()
        items: list[TreeViewModelItem] = [self.model.itemFromIndex(index) for index in selected_indices]
        selected_croco: TreeViewModelItem = items[0]
        ad: AllegroLokalnieItem = selected_croco.get_ad_item()
        if self.details is not None and ad is not None:
            self.details.set_ad(ad)
            self.details.setVisible(True)
        else:
            self.details.setVisible(False)

