import Backend as bk
from zxcvbn import zxcvbn
from random import choice, randint

from PyQt6.QtWidgets import (
    QVBoxLayout, QWidget, QPushButton, QLabel, QLineEdit, QHBoxLayout, QProgressBar, QFrame, 
)
from PyQt6.QtCore import Qt

class PasswordUtil(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet(bk.LoadStylesheet('Password'))
        
        self.LoadDict()
        self.InitUI()
        self.UpdateStrength()
    
    def InitUI(self):
        self.MainLayout = QVBoxLayout(self)
        self.MainLayout.setContentsMargins(40, 40, 40, 40)
        self.MainLayout.setSpacing(20)

        # Header
        self.Header = QLabel("Password Utilities")
        self.Header.setObjectName("ToolTitle")
        self.Header.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.MainLayout.addWidget(self.Header)

        # Input area
        self.InputArea = QFrame()
        self.InputArea.setObjectName("InputArea")
        self.InputLayout = QVBoxLayout(self.InputArea)
        self.InputLayout.setContentsMargins(20, 20, 20, 20)
        self.InputLayout.addStretch()
        
        self.EnterLabel = QLabel("Enter your password")
        self.EnterLabel.setObjectName("SubHeader")
        self.InputLayout.addWidget(self.EnterLabel)
        self.InputLayout.addStretch()

        self.PasswordBox = QLineEdit()
        self.PasswordBox.setMaxLength(70)
        self.PasswordBox.setEchoMode(QLineEdit.EchoMode.Password)
        self.PasswordBox.setPlaceholderText("Type here...")
        self.PasswordBox.textEdited.connect(self.UpdateStrength)
        self.InputLayout.addWidget(self.PasswordBox)
        self.InputLayout.addStretch()

        self.MainLayout.addWidget(self.InputArea, stretch = 4)

        # Security area
        self.SecurityArea = QFrame()
        self.SecurityArea.setObjectName("SecurityArea")
        self.SecurityLayout = QVBoxLayout(self.SecurityArea)
        self.SecurityLayout.setContentsMargins(20, 0, 20, 0)

        # Score Row
        self.SecScoreLayout = QHBoxLayout()
        self.SecScoreLabel = QLabel("Security Score:  ")
        self.SecurityScore = QLabel("0")
        self.SecurityScore.setObjectName("SecurityScore")
        self.SecScoreLayout.addWidget(self.SecScoreLabel)
        self.SecScoreLayout.addWidget(self.SecurityScore)
        self.SecScoreLayout.addStretch() 
        self.SecurityLayout.addLayout(self.SecScoreLayout)

        # Progress Bar
        self.StrengthBar = QProgressBar()
        self.StrengthBar.setTextVisible(False)
        self.StrengthBar.setRange(0, 100)
        self.SecurityLayout.addWidget(self.StrengthBar)

        # Time Row
        self.TimeLayout = QHBoxLayout()
        self.TimeLabel = QLabel("Estimated crack time:  ")
        self.TimeCracked = QLabel("-")
        self.TimeCracked.setObjectName("TimeCracked")
        self.TimeLayout.addWidget(self.TimeLabel)
        self.TimeLayout.addWidget(self.TimeCracked)
        self.TimeLayout.addStretch()
        self.SecurityLayout.addLayout(self.TimeLayout)

        self.MainLayout.addWidget(self.SecurityArea, stretch = 5)

        # Improve Area
        self.ImproveArea = QFrame()
        self.ImproveArea.setObjectName("ImproveArea")
        self.ImproveLayout = QVBoxLayout(self.ImproveArea)
        self.ImproveLayout.setContentsMargins(20, 20, 20, 20)

        self.ImproveLabel = QLabel("Take Action")
        self.ImproveLabel.setObjectName("SubHeader")
        self.ImproveLayout.addWidget(self.ImproveLabel)
        self.ImproveLayout.addStretch(2)

        self.GenerateLayout = QHBoxLayout()
        
        self.ImproveBtn = QPushButton("Improve Password")
        self.ImproveBtn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.ImproveBtn.clicked.connect(lambda: self.ImprovePassword(self.PasswordBox.text()))
        self.ImproveBtn.setObjectName("ImproveBtn")
        self.GenerateLayout.addWidget(self.ImproveBtn)
        
        self.RandomBtn = QPushButton("Random Password")
        self.RandomBtn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.RandomBtn.clicked.connect(lambda: self.ImprovePassword(""))
        self.RandomBtn.setObjectName("RandomBtn")
        self.GenerateLayout.addWidget(self.RandomBtn)

        self.ImproveLayout.addLayout(self.GenerateLayout)
        self.ImproveLayout.addStretch(1)

        self.PassOut = QLineEdit()
        self.PassOut.setReadOnly(True)
        self.PassOut.setPlaceholderText("Result will appear here...")
        self.PassOut.setObjectName("PasswordOut")
        self.ImproveLayout.addWidget(self.PassOut)

        self.MainLayout.addWidget(self.ImproveArea, stretch = 5)
        
        self.MainLayout.addStretch()
    
    def LoadDict(self):
        self.Dictionary = []
        self.Symbols = ['!', '@', '#', '$', '%', '&', '*', '+', '-']
        self.Numbers = ['1', '3', '0', '5', '8']
        with open(bk.ResourcePath('Extras/Dict.txt'), 'r') as fil:
            for a in fil:
                self.Dictionary.append(a.replace('\n', ''))
    
    def UpdateStrength(self):
        passwd = self.PasswordBox.text()
        if not passwd: 
            score_val = 0
            crack_time = "-"
        else:
            out = zxcvbn(passwd)
            score_val = int(out['score'] * 25) 
            crack_time = out['crack_times_display']['offline_slow_hashing_1e4_per_second']

        self.SecurityScore.setText(f"{score_val}/100")
        self.StrengthBar.setValue(score_val)
        self.TimeCracked.setText(crack_time)

        self.SetSecurityColor(score_val)

    def SetSecurityColor(self, score):
        if score < 25: 
            color = "#ef4444"
            self.SecurityScore.setProperty("class", "red")
        elif score < 50: 
            color = "#f97316"
            self.SecurityScore.setProperty("class", "orange")
        elif score < 75: 
            color = "#3b82f6"
            self.SecurityScore.setProperty("class", "blue")
        else: 
            color = "#22c55e"
            self.SecurityScore.setProperty("class", "green")
        
        self.SecurityScore.style().unpolish(self.SecurityScore)
        self.SecurityScore.style().polish(self.SecurityScore)
        
        self.StrengthBar.setStyleSheet(f"""
            QProgressBar::chunk {{
                background-color: {color};
            }}
        """)
    
    def ImprovePassword(self, password):
        improved = password
        while len(improved) < 14:
            improved += choice(self.Dictionary) + ' '
        
        improved = improved.strip()
        
        while True:
            info = zxcvbn(improved)
            words = [x['token'] for x in info['sequence'] if x['pattern'] == 'dictionary']
            if len(words) == 0: break

            for word in words:
                loc = randint(0, len(word) - 1)
                repl = word[:loc] + choice(self.Numbers + self.Symbols) + word[loc+1:]
                improved = improved.replace(word, repl)
        
        self.PassOut.setText(improved)
    
    def resizeEvent(self, event):
        InputHeight = self.InputArea.height()

        TextBoxHeight = int(InputHeight * 0.27)
        self.PasswordBox.setStyleSheet(f"padding: {int(TextBoxHeight * 0.15)}px;")
        self.PassOut.setStyleSheet(f"padding: {int(TextBoxHeight * 0.15)}px;")
        self.PasswordBox.setFixedHeight(TextBoxHeight)
        self.PassOut.setFixedHeight(TextBoxHeight)

        FontSize = int(InputHeight * 0.13)
        FontSizeBig = int(InputHeight * 0.17)
        self.EnterLabel.setStyleSheet(f"font-size: {FontSize}px")
        self.SecScoreLabel.setStyleSheet(f"font-size: {FontSize}px")
        self.TimeLabel.setStyleSheet(f"font-size: {FontSize}px")
        self.ImproveLabel.setStyleSheet(f"font-size: {FontSize}px")
        self.SecurityScore.setStyleSheet(f"font-size: {FontSizeBig}px")
        self.TimeCracked.setStyleSheet(f"font-size: {FontSizeBig}px")

        super().resizeEvent(event)