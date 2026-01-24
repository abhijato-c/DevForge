import Backend as bk
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QVBoxLayout, QWidget, QPushButton

class EncryptionUtil(QWidget):
    def __init__(self,):
        super().__init__()

        # Stylesheet
        self.setStyleSheet(bk.LoadStylesheet('Encryption'))