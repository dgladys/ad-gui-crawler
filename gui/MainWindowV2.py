from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QApplication, QSplitter
from gui.AdDetail import AdDetails
from gui.TreeView import AdTreeView
from scrap.allegrolokalnie import AllegroLokalnieItem



class MainWindowV2(QMainWindow):
    def __init__(self, items: list[AllegroLokalnieItem]):
        super().__init__()
        self.setWindowTitle("Crocoradar")
        #self.resize(800, 600)
        self.ad_details = AdDetails()
        tree_view = AdTreeView(items=items, details=self.ad_details)
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