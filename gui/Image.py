import requests
from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPixmap, QImage


class ExternalImage(QLabel):

    def __init__(self, url: str):
        super().__init__()
        self.load_from_url(url)

    def __create_pixmap(self, image: QImage = None, width: int = 320, height: int = 240):

        pix_map = QPixmap.fromImage(image) if image is not None else QPixmap()
        if width is not None and height is not None:
            pix_map = QPixmap.fromImage(image).scaled(width, height)
        return pix_map

    def create_empty(self, width: int = 320, height: int = 240):
        return self.__create_pixmap(width=width, height=height)

    def load_from_url(self, url_path: str, width: int = 320, height: int = 240):
        try:
            response = requests.get(url_path)
            image_data = response.content
            image = QImage()
            image.loadFromData(image_data)

            pix_map = self.__create_pixmap(image, width, height)
            self.setPixmap(pix_map)
        except Exception as e:
            print("Error during loading image")
            return False
        return True

