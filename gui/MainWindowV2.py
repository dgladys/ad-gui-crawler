from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QApplication, QSplitter, QGridLayout, QWidget
from gui.AdDetail import AdDetails
from gui.TreeView import AdTreeView
from scrap.allegrolokalnie import AllegroLokalnieItem



class MainWindow(QMainWindow):
    def __init__(self, items: list[AllegroLokalnieItem]):
        super().__init__()
        self.setWindowTitle("Crocoradar")
        self.resize(800, 600)
        layout = QGridLayout()



        self.ad_details = AdDetails()
        self.ad_details.setVisible(False)
        self.tree_view = AdTreeView(items=items, details=self.ad_details)
        layout.addWidget(self.tree_view, 0, 0)
        layout.addWidget(self.ad_details, 1, 0)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)



def main(items: list[AllegroLokalnieItem]):
    app = QApplication([])
    window = MainWindow(items)
    window.show()
    app.exec()