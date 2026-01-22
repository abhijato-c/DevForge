import Backend as bk
from PyQt6.QtWidgets import (
    QWidget, QGridLayout, QPushButton, QFrame, QScrollArea, QVBoxLayout, QLabel
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QPixmap

class HomeGrid(QScrollArea):
    ToolSelected = pyqtSignal(str) 

    def __init__(self):
        super().__init__()

        # Stylesheet
        with open(bk.ResourcePath('Styles/global.css'), "r") as f:
            stylesheet = f.read()
        with open(bk.ResourcePath('Styles/Home.css'), "r") as f:
            stylesheet += f.read()
        self.setStyleSheet(stylesheet)

        # Scroll Area
        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setFrameShape(QFrame.Shape.NoFrame)

        # Main container -> Header, tools grid
        self.container = QWidget()
        self.container.setObjectName("HomeContainer")
        self.setWidget(self.container)
        
        self.MainLayout = QVBoxLayout(self.container)
        self.MainLayout.setContentsMargins(40, 40, 40, 40)
        self.MainLayout.setSpacing(20)

        # Header
        self.HeaderContainer = QWidget()
        HeaderLayout = QVBoxLayout(self.HeaderContainer)
        HeaderLayout.setContentsMargins(0,0,0,0)
        
        title = QLabel("DevForge Utilities")
        title.setObjectName("DashboardTitle")
        HeaderLayout.addWidget(title)
        
        subtitle = QLabel("Select a utility")
        subtitle.setObjectName("DashboardSubtitle")
        HeaderLayout.addWidget(subtitle)
        
        self.MainLayout.addWidget(self.HeaderContainer)

        # tools grid
        self.GridWidget = QWidget()
        self.grid = QGridLayout(self.GridWidget)
        self.grid.setContentsMargins(0, 10, 0, 0)
        self.grid.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        
        self.MainLayout.addWidget(self.GridWidget)
        self.MainLayout.addStretch()

        self.ButtonWidgets = []
        
        # Initialize Buttons
        for name in bk.tools:
            btn = QPushButton()
            btn.setObjectName("ToolSelector")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            
            BtnLayout = QVBoxLayout(btn)
            BtnLayout.setContentsMargins(0, 0, 0, 0)
            BtnLayout.setSpacing(0)
            
            BtnLayout.addStretch(5)

            # Icon
            image = QLabel()
            image.setObjectName("ToolSelectorIcon")
            image.setScaledContents(True)
            image.setPixmap(QPixmap(bk.ResourcePath(f"Static/{name} Image.png")))
            BtnLayout.addWidget(image, alignment=Qt.AlignmentFlag.AlignHCenter)

            BtnLayout.addStretch(3)

            # Label
            label = QLabel(name)
            label.setObjectName("ToolSelectorLabel")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            BtnLayout.addWidget(label, alignment=Qt.AlignmentFlag.AlignHCenter)

            BtnLayout.addStretch(6)

            btn.clicked.connect(lambda checked, name=name: self.ToolSelected.emit(name))
            self.ButtonWidgets.append(btn)

    def resizeEvent(self, event):
        width = self.viewport().width() - 40
        height = self.viewport().height()

        MaxBtnWidth = 350
        MinBtnWidth = 150

        BtnWidth = max(min(width / 5, MaxBtnWidth), MinBtnWidth)
        Spacing = BtnWidth / 10
        Ncols = round(width / (BtnWidth + Spacing))
        BtnWidth = round((10 * width) / (Ncols * (10 + 1)))
        Spacing = round(BtnWidth / 10)
        BtnHeight = int(BtnWidth * 1.5)
        IconSize = int(BtnWidth * 0.5)
        FontSize = max(10, int(BtnWidth / 12)) 

        self.grid.setSpacing(Spacing)

        for i in range(len(self.ButtonWidgets)):
            widget = self.ButtonWidgets[i]
            widget.setStyleSheet(f"border-radius: {BtnWidth / 7}px")
            widget.setFixedSize(BtnWidth, BtnHeight)

            image = widget.findChild(QLabel, "ToolSelectorIcon")
            image.setFixedSize(IconSize, IconSize)

            label = widget.findChild(QLabel, "ToolSelectorLabel")
            label.setStyleSheet(f"font-size: {FontSize}px;")
            label.setFixedWidth(int(BtnWidth * 0.9))
            
            row, col = divmod(i, Ncols)
            self.grid.addWidget(widget, row, col)
        
        super().resizeEvent(event)