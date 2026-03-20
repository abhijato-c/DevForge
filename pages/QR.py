import Backend as bk

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QStackedWidget, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel

class QRUtil(QWidget):
    def __init__(self,):
        super().__init__()

        # Stylesheet
        self.setStyleSheet(bk.LoadStylesheet('QR'))

        self.Tabs = {}
        self.Mode = ''

        self.InitUI()
        self.ModeChanged('Create QR')
    
    def InitUI(self):
        def CreateTab(name):
            tab = QPushButton(name)
            tab.setObjectName("TabBtn")
            tab.setCursor(Qt.CursorShape.PointingHandCursor)
            tab.clicked.connect(lambda: self.ModeChanged(name))
            self.TabLayout.addWidget(tab)
            self.Tabs[name] = tab

        self.MainLayout = QVBoxLayout(self)
        self.MainLayout.setContentsMargins(30, 30, 30, 30)
        self.MainLayout.setSpacing(20)

        # Header
        self.Header = QLabel("QR & Barcode")
        self.Header.setObjectName("ToolTitle")
        self.Header.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.MainLayout.addWidget(self.Header)

        # Tabs
        self.TabContainer = QWidget()
        self.TabContainer.setObjectName("TabContainer")
        self.TabLayout = QHBoxLayout(self.TabContainer)
        self.TabLayout.setContentsMargins(5, 5, 5, 5)
        self.TabLayout.setSpacing(5)
        self.TabLayout.addStretch()

        CreateTab("Create QR")
        CreateTab("Read QR")

        self.TabLayout.addStretch()
        self.MainLayout.addWidget(self.TabContainer)

        self.ProcessArea = QStackedWidget()

        self.MainLayout.addStretch(1)
    
    def ModeChanged(self, mode):
        if self.Mode != '':
            OldTab = self.Tabs[self.Mode]
            OldTab.setProperty('active', False)
            self.RefreshStyle(OldTab)
        self.Mode = mode

        NewTab = self.Tabs[self.Mode]
        NewTab.setProperty('active', True)
        self.RefreshStyle(NewTab)

        self.ProcessArea.setCurrentIndex(list(self.Tabs.keys()).index(self.Mode))
        self.resizeEvent(None)

    def RefreshStyle(self, widget):
        widget.style().unpolish(widget)
        widget.style().polish(widget)
        widget.update()