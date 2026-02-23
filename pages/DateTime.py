import Backend as bk
import datetime

from PyQt6.QtWidgets import (
    QVBoxLayout, QWidget, QPushButton, QLabel, QHBoxLayout, QFrame, QLineEdit, QStackedWidget, QCalendarWidget
)
from PyQt6.QtCore import Qt, QDateTime, QTime
from PyQt6.QtGui import QDoubleValidator, QIntValidator

class DateTimeUtil(QWidget):
    def __init__(self):
        super().__init__()

        # Stylesheet
        self.setStyleSheet(bk.LoadStylesheet('DateTime'))

        self.LeftInputTime = 0
        self.RightInputTime = 0
        self.Mode = ""
        self.Operation = ""
        self.Tabs = {}

        self.InitUI()
        # Default state
        self.ModeChanged("Add Dates")
        self.SetOperation("+")

    def InitUI(self):
        def CreateTab(name):
            btn = QPushButton(name)
            btn.setObjectName("TabBtn")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda checked, n=name: self.ModeChanged(n))
            self.TabLayout.addWidget(btn)
            self.Tabs[name] = btn
        
        self.MainLayout = QVBoxLayout(self)
        self.MainLayout.setContentsMargins(30, 30, 30, 30)
        self.MainLayout.setSpacing(20)

        # Header
        self.Header = QLabel("Date & Time Utilities")
        self.Header.setObjectName("ToolTitle")
        self.MainLayout.addWidget(self.Header)

        # Tabs
        self.TabContainer = QWidget()
        self.TabContainer.setObjectName("TabContainer")
        self.TabLayout = QHBoxLayout(self.TabContainer)
        self.TabLayout.setContentsMargins(5, 5, 5, 5)
        self.TabLayout.setSpacing(5)

        self.TabLayout.addStretch()
        CreateTab("Add Dates")
        CreateTab("Time After Date")
        CreateTab("Time Till Date")
        self.TabLayout.addStretch()

        self.MainLayout.addWidget(self.TabContainer)

        # Input area
        self.InputArea = QFrame()
        self.InputArea.setObjectName("InputArea")
        self.InputAreaLayout = QHBoxLayout(self.InputArea)
        self.InputAreaLayout.setContentsMargins(0, 0, 0, 0)

        # Left input
        self.LeftInputStack = QStackedWidget()
        self.LeftInputStack.setObjectName("InputCard")
        self.LeftInputStack.addWidget(self.InputCardA())
        self.LeftInputStack.addWidget(self.InputCardB())
        self.InputAreaLayout.addWidget(self.LeftInputStack)

        # +- buttons container
        self.OperationSelector = QVBoxLayout()
        self.OperationSelector.setSpacing(15)
        self.OperationSelector.addStretch()

        self.PlusOperation = QPushButton('+')
        self.PlusOperation.setObjectName("Operation")
        self.PlusOperation.setProperty("class", "success")
        self.PlusOperation.setCursor(Qt.CursorShape.PointingHandCursor)
        self.PlusOperation.clicked.connect(lambda: self.SetOperation("+"))
        self.OperationSelector.addWidget(self.PlusOperation)

        self.MinusOperation = QPushButton('-')
        self.MinusOperation.setObjectName("Operation")
        self.MinusOperation.setProperty("class", "danger")
        self.MinusOperation.setCursor(Qt.CursorShape.PointingHandCursor)
        self.MinusOperation.clicked.connect(lambda: self.SetOperation("-"))
        self.OperationSelector.addWidget(self.MinusOperation)

        self.OperationSelector.addStretch()
        self.InputAreaLayout.addLayout(self.OperationSelector)

        # Right input
        self.RightInputStack = QStackedWidget()
        self.RightInputStack.setObjectName("InputCard")
        self.RightInputStack.addWidget(self.InputCardA())
        self.RightInputStack.addWidget(self.InputCardB())
        self.InputAreaLayout.addWidget(self.RightInputStack)

        # Output area
        self.OutputArea = QFrame()
        self.OutputLayout = QVBoxLayout(self.OutputArea)
        self.OutputArea.setObjectName("OutputArea")
        
        self.OutputLayout.setContentsMargins(20, 20, 20, 20)
        self.OutputLayout.setSpacing(10)

        self.OutputQuestionLabel = QLabel()
        self.OutputQuestionLabel.setObjectName("OutputQlabel")
        self.OutputLayout.addWidget(self.OutputQuestionLabel, alignment=Qt.AlignmentFlag.AlignCenter)

        self.OutputAnswerLabel = QLabel()
        self.OutputAnswerLabel.setObjectName("OutputAlabel")
        self.OutputLayout.addWidget(self.OutputAnswerLabel, alignment=Qt.AlignmentFlag.AlignCenter)

        self.MainLayout.addWidget(self.InputArea, stretch = 5)
        self.MainLayout.addWidget(self.OutputArea, stretch = 2)
        self.MainLayout.addStretch()
    
    def SetOperation(self, operation):
        self.Operation = operation

        self.PlusOperation.setProperty("active", operation == "+")
        self.PlusOperation.style().unpolish(self.PlusOperation)
        self.PlusOperation.style().polish(self.PlusOperation)

        self.MinusOperation.setProperty("active", operation == "-")
        self.MinusOperation.style().unpolish(self.MinusOperation)
        self.MinusOperation.style().polish(self.MinusOperation)
        
        self.UpdateOutput()
    
    def InputCardA(self):
        def AddRow(name):
            InputLayout = QHBoxLayout()
            InputLabel = QLabel(name)
            InputLabel.setObjectName("DurationLabel")
            InputLayout.addWidget(InputLabel)
            Input = QLineEdit("0")
            Input.setObjectName("DurationInput")
            Input.setAlignment(Qt.AlignmentFlag.AlignRight)
            Input.setValidator(QDoubleValidator())
            Input.textEdited.connect(self.UpdateInputs)
            InputLayout.addWidget(Input)
            layout.addLayout(InputLayout)

        container = QFrame()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        AddRow("Years")
        AddRow("Months")
        AddRow("Days")
        AddRow("Hours")
        AddRow("Minutes")
        AddRow("Seconds")

        return container

    def InputCardB(self):
        def AddTimeBox(placeholder):
            inp = QLineEdit()
            inp.setPlaceholderText(placeholder)
            inp.setAlignment(Qt.AlignmentFlag.AlignCenter)
            inp.setValidator(QIntValidator())
            inp.textEdited.connect(self.UpdateInputs)
            TimeLayout.addWidget(inp)
        
        container = QFrame()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        calendar = QCalendarWidget()
        calendar.setGridVisible(True)
        calendar.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader) # Cleaner look
        calendar.selectionChanged.connect(self.UpdateInputs)
        layout.addWidget(calendar)

        TimeLayout = QHBoxLayout()
        TimeLayout.setSpacing(10)
        AddTimeBox("HH")
        TimeLayout.addWidget(QLabel(":"))
        AddTimeBox("MM")
        TimeLayout.addWidget(QLabel(":"))
        AddTimeBox("SS")

        layout.addLayout(TimeLayout)

        return container
    
    def ModeChanged(self, mode):
        self.Mode = mode
        for name, tab in self.Tabs.items():
            tab.setProperty("active", name == mode)
            tab.style().unpolish(tab)
            tab.style().polish(tab)
        
        self.PlusOperation.setText("+")
        self.MinusOperation.setText("-")
        
        if mode == "Add Dates":
            self.LeftInputStack.setCurrentIndex(0)
            self.RightInputStack.setCurrentIndex(0)
        elif mode == "Time After Date":
            self.LeftInputStack.setCurrentIndex(1)
            self.RightInputStack.setCurrentIndex(0)
        elif mode == "Time Till Date":
            self.LeftInputStack.setCurrentIndex(1)
            self.RightInputStack.setCurrentIndex(1)
            self.PlusOperation.setText("→")
            self.MinusOperation.setText("←")
        self.UpdateInputs()
        self.UpdateOutput()
    
    def UpdateInputs(self):
        LFrame = self.LeftInputStack.currentWidget()
        RFrame = self.RightInputStack.currentWidget()

        if self.Mode == "Add Dates":
            vals = [float(a.text()) if a.text() else 0.0 for a in LFrame.findChildren(QLineEdit)]
            self.LeftInputTime = 0
            self.LeftInputTime += vals[0] * 31536000
            self.LeftInputTime += vals[1] * 2592000
            self.LeftInputTime += vals[2] * 86400
            self.LeftInputTime += vals[3] * 3600
            self.LeftInputTime += vals[4] * 60
            self.LeftInputTime += vals[5] * 1
            
            vals = [float(a.text()) if a.text() else 0.0 for a in RFrame.findChildren(QLineEdit)]
            self.RightInputTime = 0
            self.RightInputTime += vals[0] * 31536000
            self.RightInputTime += vals[1] * 2592000
            self.RightInputTime += vals[2] * 86400
            self.RightInputTime += vals[3] * 3600
            self.RightInputTime += vals[4] * 60
            self.RightInputTime += vals[5] * 1
        
        elif self.Mode == "Time After Date":
            vals = [int(a.text()) if a.text() else 0 for a in LFrame.findChildren(QLineEdit)]
            CalDate = QDateTime(LFrame.findChild(QCalendarWidget).selectedDate(), QTime(vals[1], vals[2], vals[3]))
            self.LeftInputTime = CalDate.toSecsSinceEpoch()

            vals = [float(a.text()) if a.text() else 0.0 for a in RFrame.findChildren(QLineEdit)]
            self.RightInputTime = 0
            self.RightInputTime += vals[0] * 31536000
            self.RightInputTime += vals[1] * 2592000
            self.RightInputTime += vals[2] * 86400
            self.RightInputTime += vals[3] * 3600
            self.RightInputTime += vals[4] * 60
            self.RightInputTime += vals[5] * 1
        
        elif self.Mode == "Time Till Date":
            vals = [int(a.text()) if a.text() else 0 for a in LFrame.findChildren(QLineEdit)]
            CalDate = QDateTime(LFrame.findChild(QCalendarWidget).selectedDate(), QTime(vals[1], vals[2], vals[3]))
            self.LeftInputTime = CalDate.toSecsSinceEpoch()

            vals = [int(a.text()) if a.text() else 0 for a in RFrame.findChildren(QLineEdit)]
            CalDate = QDateTime(RFrame.findChild(QCalendarWidget).selectedDate(), QTime(vals[1], vals[2], vals[3]))
            self.RightInputTime = CalDate.toSecsSinceEpoch()

        if self.LeftInputTime > datetime.timedelta.max.total_seconds() - 1: self.LeftInputTime = 0
        if self.RightInputTime > datetime.timedelta.max.total_seconds() - 1: self.RightInputTime = 0
        self.UpdateOutput()
    
    def UpdateOutput(self):
        if self.Mode == "Add Dates":
            LeftDate = datetime.timedelta(0, self.LeftInputTime)
            RightDate = datetime.timedelta(0, self.RightInputTime)
            try: 
                if self.Operation == "+": ans = LeftDate + RightDate
                else: ans = LeftDate - RightDate
            except: ans = datetime.timedelta(0,0)

            self.OutputQuestionLabel.setText(f"{str(LeftDate)} {self.Operation} {str(RightDate)} is")
            self.OutputAnswerLabel.setText(str(ans))
            
        elif self.Mode == "Time After Date":
            LeftDate = datetime.datetime.fromtimestamp(self.LeftInputTime)
            RightDate = datetime.timedelta(0, self.RightInputTime)
            try: 
                if self.Operation == "+": ans = LeftDate + RightDate
                else: ans = LeftDate - RightDate
            except: ans = datetime.timedelta(0,0)

            self.OutputQuestionLabel.setText(f"{str(LeftDate)} {self.Operation} {str(RightDate)} is")
            self.OutputAnswerLabel.setText(str(ans))
        
        elif self.Mode == "Time Till Date":
            LeftDate = datetime.datetime.fromtimestamp(self.LeftInputTime if self.Operation == "+" else self.RightInputTime)
            RightDate = datetime.datetime.fromtimestamp(self.RightInputTime if self.Operation == "+" else self.LeftInputTime)
            ans = RightDate - LeftDate

            self.OutputQuestionLabel.setText(f"{str(LeftDate)} - {str(RightDate)} is")
            self.OutputAnswerLabel.setText(str(ans))
    
    def resizeEvent(self, event):
        width = self.width()
        height = self.height()

        InputHeight = self.InputArea.height()

        ModeBtnSize = int(InputHeight * 0.2)
        InputCardWidth = int(width * 0.4)
        self.LeftInputStack.setFixedWidth(InputCardWidth)
        self.RightInputStack.setFixedWidth(InputCardWidth)
        self.PlusOperation.setFixedSize(ModeBtnSize, ModeBtnSize)
        self.MinusOperation.setFixedSize(ModeBtnSize, ModeBtnSize)
        self.PlusOperation.setStyleSheet(f"font-size: {int(ModeBtnSize * 0.5)}px")
        self.MinusOperation.setStyleSheet(f"font-size: {int(ModeBtnSize * 0.5)}px")

        InputFieldWidth = int(InputCardWidth * 0.6)
        InputFieldHeight = int(InputHeight * 0.12)
        InputLabelWidth = int(InputCardWidth * 0.2)
        for inp in self.LeftInputStack.findChildren(QLineEdit, "DurationInput"):
            inp.setFixedSize(InputFieldWidth, InputFieldHeight)
        for inp in self.RightInputStack.findChildren(QLineEdit, "DurationInput"):
            inp.setFixedSize(InputFieldWidth, InputFieldHeight)
        for label in self.LeftInputStack.findChildren(QLabel, "DurationLabel"):
            label.setFixedSize(InputLabelWidth, InputFieldHeight)
        for label in self.RightInputStack.findChildren(QLabel, "DurationLabel"):
            label.setFixedSize(InputLabelWidth, InputFieldHeight)

        
        super().resizeEvent(event)