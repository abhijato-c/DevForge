import Backend as bk
from random import choice, randint

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QPushButton, QTextEdit, QLabel, QHBoxLayout, QSpinBox

class LoremUtil(QWidget):
    def __init__(self):
        super().__init__()
        self.ReadDictionary()

        # Stylesheet
        self.setStyleSheet(bk.LoadStylesheet('Lorem'))

        # Main Layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(40, 40, 40, 40)
        self.layout.setSpacing(20)

        # Header
        self.header = QLabel("Lorem Ipsum Generator")
        self.header.setObjectName("ToolTitle")
        self.layout.addWidget(self.header)

        # Controls
        self.ControlsLayout = QHBoxLayout()
        self.ControlsLayout.setSpacing(15)

        self.CountLabel = QLabel("Number of words:")
        self.CountLabel.setObjectName("ControlLabel")
        self.ControlsLayout.addWidget(self.CountLabel)

        self.WordCount = QSpinBox()
        self.WordCount.setRange(1, 2000)
        self.WordCount.setValue(100)
        self.WordCount.setFixedWidth(100)
        self.WordCount.setObjectName("LoremSpinBox")
        self.WordCount.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)
        self.ControlsLayout.addWidget(self.WordCount)

        self.GenerateBtn = QPushButton("Generate Text")
        self.GenerateBtn.setObjectName("ActionBtn")
        self.GenerateBtn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.GenerateBtn.clicked.connect(self.GenerateClicked)
        self.ControlsLayout.addWidget(self.GenerateBtn)

        self.ControlsLayout.addStretch()
        self.layout.addLayout(self.ControlsLayout)

        # Output box
        self.OutBox = QTextEdit()
        self.OutBox.setObjectName("LoremOutput")
        self.OutBox.setReadOnly(True)
        self.OutBox.setPlaceholderText("Generated text will appear here...")
        self.layout.addWidget(self.OutBox)

        # Preload text
        self.GenerateClicked()

    def GenerateClicked(self):
        n = self.WordCount.value()
        result = self.GenerateText(n)
        self.OutBox.setPlainText(result)
    
    def ReadDictionary(self):
        self.Starting = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
        path = bk.ResourcePath('Extras/Lipsum.txt')
        with open(path, 'r') as dictionary:
            self.Dictionary = dictionary.read().split('\n')
    
    def GenerateText(self, Nwords):
        if Nwords<19:
            return " ".join(self.Starting.split(' ')[:Nwords])
        elif Nwords == 19:
            return self.Starting
        else:
            Ngenerate = Nwords - 19
            generated = []
            LastPeriod = True
            for i in range(Ngenerate):
                word = choice(self.Dictionary)
                if LastPeriod: 
                    word = word.capitalize()
                    LastPeriod = False
                elif randint(0,10) == 0: 
                    word += ','
                elif randint(0,6) == 0: 
                    word += '.'
                    LastPeriod = True
                
                generated.append(word)
            return self.Starting + " " + " ".join(generated)