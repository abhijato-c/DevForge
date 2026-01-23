import Backend as bk
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QVBoxLayout, QWidget, QPushButton

class MarkdownUtil(QWidget):
    def __init__(self, HomeCallback):
        super().__init__()

        # Stylesheet
        self.setStyleSheet(bk.LoadStylesheet('md'))