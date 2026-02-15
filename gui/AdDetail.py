from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QColor, QDesktopServices
from PyQt6.QtWidgets import QSplitter, QLabel, QPushButton, QGridLayout, QWidget

from gui.Image import ExternalImage
from scrap.allegrolokalnie import AllegroLokalnieItem


class ASplitter(QSplitter):
    def set_background_color(self, color: str):
        palette = self.palette()
        role = self.backgroundRole()
        palette.setColor(role, QColor(color))
        self.setPalette(palette)
        self.setObjectName('AdDescription')
        self.setStyleSheet("#AdDescription{background-color: "+color+";}")

class AdDescription(QWidget):

    def __create_bold_label(self, text):
        label = QLabel(text)
        font = label.font()
        font.setBold(True)
        label.setFont(font)
        return label

    def __init__(self, parent=None):
        super().__init__(parent)

        #Itself configuration
        #self.setOrientation(Qt.Orientation.Vertical)
        #self.set_background_color("#FFFFFF")
        self.ad = None

        #Items
        self.gridLayout = QGridLayout()

        self.titleLabel = self.__create_bold_label("Tytuł")
        self.descriptionLabel = self.__create_bold_label("Cos")
        self.priceLabel = self.__create_bold_label("Cena")
        self.urlLabel = self.__create_bold_label("URL")


        self.title = QLabel()
        self.description = QLabel()
        self.price = QLabel()
        self.url = QLabel()
        self.button = QPushButton("Otwórz w przeglądarce", self)

        self.gridLayout.addWidget(self.titleLabel, 0, 0)
        self.gridLayout.addWidget(self.descriptionLabel, 1, 0)
        self.gridLayout.addWidget(self.priceLabel, 2, 0)
        self.gridLayout.addWidget(self.urlLabel, 3, 0)


        self.gridLayout.addWidget(self.title, 0, 1)
        self.gridLayout.addWidget(self.description, 1, 1)
        self.gridLayout.addWidget(self.price, 2, 1)
        self.gridLayout.addWidget(self.url, 3, 1)
        self.gridLayout.addWidget(self.button, 4, 0, 1, 2)
        #self.gridLayout.addWidget(self.button, 1, 0, 1, 2)
        self.setLayout(self.gridLayout)
        self.button.clicked.connect(lambda p: self.on_button_pressed(p))



    def set_ad(self, ad: AllegroLokalnieItem):
        self.ad = ad
        print(ad, "set_ad")
        if isinstance(ad, AllegroLokalnieItem):
            print("SET!!!")
            self.title.setText(ad.get_title())
            self.description.setText(ad.get_full_price())
            self.price.setText(ad.get_full_price())
            self.url.setText(ad.get_link())

    def on_button_pressed(self, button):
        QDesktopServices.openUrl(QUrl(self.ad.get_link()))


class AdDetails(ASplitter):

    def __init__(self):
        super().__init__()
        self.setOrientation(Qt.Orientation.Horizontal)
        self.set_background_color("#FFFFFF")
        self.image = ExternalImage('https://a.allegroimg.com/s180x180/1199be/f7e42f93403f8b2c76076c04235f')
        self.image.resize(320, 240)
        self.addWidget(self.image)
        self.ad = None
        self.description = AdDescription(parent=self)


    def set_ad(self, ad: AllegroLokalnieItem):
        self.ad = ad
        if self.ad is not None and self.ad.get_image():
            self.image.load_from_url(url_path=ad.get_image())
            self.description.set_ad(ad)
        else:
            self.image.create_empty()
