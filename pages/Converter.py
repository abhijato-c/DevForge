import Backend as bk
from pandas import read_csv

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QFrame, QScrollArea, QMenu, QWidgetAction, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDoubleValidator

class ConverterUtil(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("ConverterPage")
        
        self.IsUpdating = False
        
        self.setStyleSheet(bk.LoadStylesheet("Converter"))

        self.TopUnit = ""
        self.BottomUnit = ""
        self.ConverterSelected = "Top"
        self.InitData()
        self.InitUI()
        self.PopulateUnits()

    def InitData(self):
        self.UnitsDB = {}

        data = read_csv(bk.ResourcePath("Extras/Converter.csv"))
        for index, row in data.iterrows():
            if row['Mode'] not in self.UnitsDB: self.UnitsDB[row['Mode']] = {}
            self.UnitsDB[row['Mode']][row['Name']] = {"Abbr": row['Abbr'], "Factor": row['Factor']}

    def InitUI(self):
        self.MainLayout = QVBoxLayout(self)
        self.MainLayout.setContentsMargins(30, 30, 30, 30)
        self.MainLayout.setSpacing(20)

        # Header
        self.Header = QLabel("Unit Converter")
        self.Header.setObjectName("ToolTitle")
        self.MainLayout.addWidget(self.Header)

        # Unit menu
        self.UnitMenu = QMenu()
        self.UnitMenu.setObjectName("UnitMenu")

        self.UnitScrollArea = QScrollArea()
        self.UnitScrollArea.setObjectName("UnitScrollArea")
        self.UnitScrollArea.setWidgetResizable(True)
        self.UnitScrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.UnitScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.UnitScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.UnitScrollArea.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.UnitScrollContainer = QWidget()
        self.UnitScrollContainer.setObjectName("UnitScrollContainer")
        self.UnitScrollLayout = QVBoxLayout(self.UnitScrollContainer)
        self.UnitScrollLayout.setObjectName("UnitScrollLayout")
        self.UnitScrollLayout.setContentsMargins(5, 5, 5, 5)
        self.UnitScrollLayout.setSpacing(2)

        self.UnitScrollArea.setWidget(self.UnitScrollContainer)

        action = QWidgetAction(self.UnitMenu)
        action.setDefaultWidget(self.UnitScrollArea)
        self.UnitMenu.addAction(action)

        # Converter card
        self.Card = QFrame()
        self.Card.setObjectName("ConverterCard")
        self.CardLayout = QVBoxLayout(self.Card)
        self.CardLayout.setContentsMargins(40, 40, 40, 40)
        self.CardLayout.setSpacing(15)

        # Mode dropdown
        self.ModeLayout = QHBoxLayout()
        self.ModeLabel = QLabel("Conversion Mode:")
        self.ModeLabel.setObjectName("SubLabel")
        self.ModeCombo = QComboBox()
        self.ModeCombo.addItems(list(self.UnitsDB.keys()))
        self.ModeCombo.setObjectName("ModeCombo")
        self.ModeCombo.setCursor(Qt.CursorShape.PointingHandCursor)
        self.ModeCombo.currentTextChanged.connect(self.PopulateUnits)
        
        self.ModeLayout.addWidget(self.ModeLabel)
        self.ModeLayout.addWidget(self.ModeCombo)
        self.ModeLayout.addStretch()
        self.CardLayout.addLayout(self.ModeLayout)

        # Top input row
        self.TopRow = QHBoxLayout()
        self.TopRow.setSpacing(0)
        
        self.TopInput = QLineEdit("1")
        self.TopInput.setObjectName("ConvInput")
        self.TopInput.setValidator(QDoubleValidator())
        self.TopInput.textEdited.connect(lambda: self.Convert("Top"))
        self.TopInput.setFixedHeight(50)
        self.TopRow.addWidget(self.TopInput)

        self.TopUnitSel = QPushButton()
        self.TopUnitSel.setObjectName("UnitSelector")
        self.TopUnitSel.setCursor(Qt.CursorShape.PointingHandCursor)
        self.TopUnitSel.clicked.connect(lambda: self.ShowMenu("Top"))
        self.TopUnitSel.setFixedHeight(50)
        self.TopRow.addWidget(self.TopUnitSel)

        self.CardLayout.addLayout(self.TopRow)

        # Top rate label
        self.TopRateLabel = QLabel("")
        self.TopRateLabel.setObjectName("RateLabel")
        self.TopRateLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.CardLayout.addWidget(self.TopRateLabel)

        # = sign
        self.EqLabel = QLabel("=")
        self.EqLabel.setObjectName("EqualsLabel")
        self.EqLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.CardLayout.addWidget(self.EqLabel)

        # Bottom input row
        self.BottomRow = QHBoxLayout()
        self.BottomRow.setSpacing(0)

        self.BottomInput = QLineEdit()
        self.BottomInput.setObjectName("ConvInput")
        self.BottomInput.setValidator(QDoubleValidator())
        self.BottomInput.textEdited.connect(lambda: self.Convert("Bottom"))
        self.BottomInput.setFixedHeight(50)
        self.BottomRow.addWidget(self.BottomInput)

        self.BottomUnitSel = QPushButton()
        self.BottomUnitSel.setObjectName("UnitSelector")
        self.BottomUnitSel.setCursor(Qt.CursorShape.PointingHandCursor)
        self.BottomUnitSel.clicked.connect(lambda: self.ShowMenu("Bottom"))
        self.BottomUnitSel.setFixedHeight(50)
        self.BottomRow.addWidget(self.BottomUnitSel)

        self.CardLayout.addLayout(self.BottomRow)

        # Bottom rate label
        self.BottomRateLabel = QLabel()
        self.BottomRateLabel.setObjectName("RateLabel")
        self.BottomRateLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.CardLayout.addWidget(self.BottomRateLabel)

        self.MainLayout.addWidget(self.Card)
        self.MainLayout.addStretch()
    
    def ShowMenu(self, TopBottom):
        self.ConverterSelected = TopBottom
        btn = self.TopUnitSel if TopBottom == "Top" else self.BottomUnitSel
        Position = btn.mapToGlobal(btn.rect().bottomLeft())
        SelectedAction = self.UnitMenu.exec(Position)

    def PopulateUnits(self):
        Mode = self.ModeCombo.currentText()
        UnitsData = self.UnitsDB[Mode]
        
        # Update to defaults
        self.UnitMenu.close()
        self.TopUnit =  next(iter(UnitsData))
        self.BottomUnit = next(iter(UnitsData))
        self.TopUnitSel.setText(self.UnitsDB[Mode][self.TopUnit]['Abbr'])
        self.BottomUnitSel.setText(self.UnitsDB[Mode][self.BottomUnit]['Abbr'])
        self.UpdateRateLabels()
        self.Convert("Top")

        # Clear units
        while self.UnitScrollLayout.count():
            item = self.UnitScrollLayout.takeAt(0)
            widget = item.widget()
            widget.deleteLater()

        for name, info in UnitsData.items():
            Button = QPushButton(name)
            Button.setObjectName("UnitMenuOption")
            Button.setCursor(Qt.CursorShape.PointingHandCursor)
            Button.clicked.connect(lambda checked, n=name: self.SetUnit(self.ConverterSelected, n))
            self.UnitScrollLayout.addWidget(Button)
    
    def SetUnit(self, TopBottom, unit):
        if TopBottom == "Top":
            self.TopUnit = unit
            self.TopUnitSel.setText(self.UnitsDB[self.ModeCombo.currentText()][unit]['Abbr'])
        else:
            self.BottomUnit = unit
            self.BottomUnitSel.setText(self.UnitsDB[self.ModeCombo.currentText()][unit]['Abbr'])

        self.UnitMenu.close()

        self.UpdateRateLabels()
        self.Convert("Top")

    def UpdateRateLabels(self):
        Mode = self.ModeCombo.currentText()

        # Get Abbr from UserData
        TopAbbr = self.UnitsDB[Mode][self.TopUnit]['Abbr']
        BottomAbbr = self.UnitsDB[Mode][self.BottomUnit]['Abbr']

        val = self.Calculate(1.0, self.TopUnit, self.BottomUnit, Mode)
        self.TopRateLabel.setText(f"1 {TopAbbr} = {val:.4g} {BottomAbbr}")
        val = self.Calculate(1.0, self.BottomUnit, self.TopUnit, Mode)
        self.BottomRateLabel.setText(f"1 {BottomAbbr} = {val:.4g} {TopAbbr}")

    def Convert(self, Source):
        if self.IsUpdating: return
        self.IsUpdating = True

        Mode = self.ModeCombo.currentText()

        if Source == "Top":
            InputWidget = self.TopInput
            OutputWidget = self.BottomInput
            FromUnit = self.TopUnit
            ToUnit = self.BottomUnit
        else:
            InputWidget = self.BottomInput
            OutputWidget = self.TopInput
            FromUnit = self.BottomUnit
            ToUnit = self.TopUnit

        ValStr = InputWidget.text()
        if not ValStr or ValStr == "-": ValStr = "0"
        Value = float(ValStr)

        Result = self.Calculate(Value, FromUnit, ToUnit, Mode)

        ResStr = f"{Result:.4f}".rstrip('0').rstrip('.')
        if ResStr == "": ResStr = "0"
        OutputWidget.setText(ResStr)

        self.IsUpdating = False

    def Calculate(self, Value, FromName, ToName, Mode):
        Data = self.UnitsDB[Mode]
        
        if Mode == "Temperature":
            return self.ConvertTemp(Value, FromName, ToName)
        else:
            FactorFrom = Data[FromName]['Factor']
            FactorTo = Data[ToName]['Factor']
            BaseVal = Value * FactorFrom
            return BaseVal / FactorTo

    def ConvertTemp(self, Val, From, To):
        C = Val
        if From == "Fahrenheit": C = (Val - 32) * 5/9
        elif From == "Kelvin": C = Val - 273.15
        
        if To == "Fahrenheit": return (C * 9/5) + 32
        elif To == "Kelvin": return C + 273.15
        return C