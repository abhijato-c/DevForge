import sys
import Backend as bk

from Home import HomeGrid
from pages.Hash import HashUtil

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QFrame, QScrollArea, QPushButton
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DevForge")
        self.resize(700, 500)

        # Stylesheet
        with open(bk.ResourcePath('Styles/global.css'), "r") as f:
            stylesheet = f.read()
        with open(bk.ResourcePath('Styles/main.css'), "r") as f:
            stylesheet += f.read()
        self.setStyleSheet(stylesheet)

        # Setup
        self.CentralWidget = QWidget()
        self.setCentralWidget(self.CentralWidget)
        self.MainLayout = QHBoxLayout(self.CentralWidget)
        self.MainLayout.setContentsMargins(0, 0, 0, 0)
        self.MainLayout.setSpacing(0)

        self.SetupSidebar()
        self.SetupStack()
    
    def SetupSidebar(self):
        self.sidebar = QWidget()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(240)
        SidebarLayout = QVBoxLayout(self.sidebar)
        SidebarLayout.setContentsMargins(0, 0, 0, 0)
        SidebarLayout.setSpacing(0)

        # Sidebar Title
        title = QLabel("DEVFORGE")
        title.setObjectName("SidebarTitle")
        title.setFixedHeight(70)
        title.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        SidebarLayout.addWidget(title)

        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        ScrollContent = QWidget()
        ScrollContent.setObjectName("SidebarScrollContent")
        self.ScrollLayout = QVBoxLayout(ScrollContent)
        self.ScrollLayout.setContentsMargins(10, 10, 10, 10)
        self.ScrollLayout.setSpacing(4)
        self.ScrollLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Home button
        HomeButton = self.CreateNavBtn("Home", "Home Icon")
        HomeButton.clicked.connect(lambda: self.SwitchTool(""))
        self.ScrollLayout.addWidget(HomeButton)

        # Separator Line
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setObjectName("SidebarSeparator")
        self.ScrollLayout.addWidget(line)

        # Nav buttons
        for name in bk.tools:
            btn = self.CreateNavBtn(name, name+" Icon")
            btn.clicked.connect(lambda checked, n=name: self.SwitchTool(n))
            self.ScrollLayout.addWidget(btn)

        scroll.setWidget(ScrollContent)
        SidebarLayout.addWidget(scroll)
        self.MainLayout.addWidget(self.sidebar)
    
    def SetupStack(self):
        self.stack = QStackedWidget()
        self.MainLayout.addWidget(self.stack)

        # HomePage
        self.home = HomeGrid()
        self.home.ToolSelected.connect(self.SwitchTool)
        self.stack.addWidget(self.home)
        
        # Stack tools
        self.HashUtil = HashUtil(HomeCallback = lambda: self.SwitchTool(""))
        self.stack.addWidget(self.HashUtil)

    def CreateNavBtn(self, text, icon):
        btn = QPushButton(f"  {text}")
        btn.setObjectName("SidebarBtn")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setHeight = 45
        
        # Icon
        btn.setIcon(QIcon(bk.ResourcePath(f"Static/{icon}.png")))
        btn.setIconSize(QSize(20, 20))
            
        return btn

    def SwitchTool(self, name):
        try:
            index = bk.tools.index(name) + 1
            self.stack.setCurrentIndex(index)
        except (ValueError, IndexError):
            self.stack.setCurrentIndex(0) # Fallback to home

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setDesktopFileName("DevForge")
    #app.setWindowIcon(QIcon(bk.ResourcePath('logo.ico')))
    app.setStyle("Fusion")

    window = MainWindow()
    window.show()
    sys.exit(app.exec())