import requests
from PyQt6.QtWidgets import QLabel, QApplication, QSizePolicy
from PyQt6.QtGui import QPixmap, QImage


class ExternalImage(QLabel):

    def __init__(self, url: str):
        super().__init__()
        self.load_from_url(url)

    def load_from_url(self, url_path: str):
        try:
            response = requests.get(url_path)
            image_data = response.content
            image = QImage()
            image.loadFromData(image_data)
            self.setPixmap(QPixmap.fromImage(image))
            self.setScaledContents(True)
            self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored )
        except Exception as e:
            print("Error during loading image")
            return False
        return True


class ImageFactory:

    @staticmethod
    def create_from_url(url_path: str) -> ExternalImage:
        return ExternalImage(url_path)
