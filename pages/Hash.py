
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QVBoxLayout, QWidget, QPushButton

class HashUtil(QWidget):
    def __init__(self, HomeCallback):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QPushButton("Back to Home", clicked=HomeCallback))
        layout.addWidget(QPushButton("Calculate SHA-256 (Placeholder)"))