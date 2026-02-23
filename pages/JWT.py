import Backend as bk
import json
import hmac
from hashlib import sha256, sha384, sha512
from base64 import urlsafe_b64decode, urlsafe_b64encode
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QPushButton, QLabel, QHBoxLayout, QFrame, QTextEdit, QComboBox

class JWTUtil(QWidget):
    def __init__(self,):
        super().__init__()
        self.ENCODING = 'utf-8'

        # Stylesheet
        self.setStyleSheet(bk.LoadStylesheet('JWT'))

        self.HashAlgos = {"HS256": sha256, "HS384": sha384, "HS512": sha512}
        self.InitUI()

        self.ModeChanged("Decode")
        with open(bk.ResourcePath("Extras/JWT.txt"), "r") as f:
            text = f.read().splitlines()
        
        self.JWTtext.blockSignals(True)
        self.KeyText.blockSignals(True)

        self.JWTtext.setText(text[0])
        self.KeyText.setText(text[1])

        self.JWTtext.blockSignals(False)
        self.KeyText.blockSignals(False)

        self.UpdateOutput()
    
    def InitUI(self):
        def CreateValBox():
            Box = QFrame()
            Box.setObjectName("ValBox")
            BoxLayout = QHBoxLayout(Box)
            BoxLayout.setContentsMargins(10, 0, 0, 0)

            Icon = QLabel()
            Icon.setScaledContents(True)
            BoxLayout.addWidget(Icon, alignment = Qt.AlignmentFlag.AlignVCenter)

            ValText = QLabel()
            BoxLayout.addWidget(ValText)

            Box.icon = Icon
            Box.text = ValText

            return Box
        
        self.MainLayout = QVBoxLayout(self)
        self.MainLayout.setContentsMargins(30, 30, 30, 30)
        self.MainLayout.setSpacing(20)

        # Header
        self.Header = QLabel("JWT Utilities")
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

        self.DecodeTab = QPushButton("Decode")
        self.DecodeTab.setObjectName("TabBtn")
        self.DecodeTab.setCursor(Qt.CursorShape.PointingHandCursor)
        self.DecodeTab.clicked.connect(lambda: self.ModeChanged("Decode"))
        self.TabLayout.addWidget(self.DecodeTab)

        self.EncodeTab = QPushButton("Encode")
        self.EncodeTab.setObjectName("TabBtn")
        self.EncodeTab.setCursor(Qt.CursorShape.PointingHandCursor)
        self.EncodeTab.clicked.connect(lambda: self.ModeChanged("Encode"))
        self.TabLayout.addWidget(self.EncodeTab)

        self.TabLayout.addStretch()
        self.MainLayout.addWidget(self.TabContainer)

        # Processing area
        self.ProcessLayout = QHBoxLayout()

        # JWT and keys etc
        self.JWTrow = QVBoxLayout()

        self.InpContainer = QWidget()
        self.InpRow = QVBoxLayout(self.InpContainer)
        self.JWTlabel = QLabel("JSON Web Token (JWT): ")
        self.JWTlabel.setObjectName("bold")
        self.InpRow.addWidget(self.JWTlabel)
        self.JWTtext = QTextEdit()
        self.JWTtext.textChanged.connect(self.UpdateOutput)
        self.InpRow.addWidget(self.JWTtext)

        self.Keylabel = QLabel("Validating Key: ")
        self.Keylabel.setObjectName("bold")
        self.InpRow.addWidget(self.Keylabel)
        self.KeyText = QTextEdit()
        self.KeyText.textChanged.connect(self.UpdateOutput)
        self.InpRow.addWidget(self.KeyText)
        self.JWTrow.addWidget(self.InpContainer, stretch = 10)

        # Validation row
        self.ValContainer = QWidget()
        self.ValRow = QVBoxLayout(self.ValContainer)

        self.JWTval = CreateValBox()
        self.ValRow.addWidget(self.JWTval)

        self.HeaderBase64Val = CreateValBox()
        self.ValRow.addWidget(self.HeaderBase64Val)

        self.PayloadBase64Val = CreateValBox()
        self.ValRow.addWidget(self.PayloadBase64Val)

        self.KeyFormatVal = CreateValBox()
        self.ValRow.addWidget(self.KeyFormatVal)

        self.SignatureVal = CreateValBox()
        self.ValRow.addWidget(self.SignatureVal)

        self.JWTrow.addWidget(self.ValContainer, stretch = 8)
        self.ProcessLayout.addLayout(self.JWTrow)

        # Decoded data
        self.DataRow = QVBoxLayout()

        self.HashLayout = QHBoxLayout()
        self.HashLabel = QLabel("Signing Function: ")
        self.HashLabel.setObjectName("bold")
        self.HashLayout.addWidget(self.HashLabel)
        self.HashFunc = QComboBox()
        self.HashFunc.addItems(self.HashAlgos.keys())
        self.HashFunc.currentTextChanged.connect(self.UpdateOutput)
        self.HashLayout.addWidget(self.HashFunc, alignment = Qt.AlignmentFlag.AlignRight)
        self.DataRow.addLayout(self.HashLayout)

        self.HeaderTop = QHBoxLayout()
        self.HeaderLabel = QLabel("Header: ")
        self.HeaderLabel.setObjectName("bold")
        self.HeaderTop.addWidget(self.HeaderLabel, stretch = 2)
        self.HeaderJsonVal = CreateValBox()
        self.HeaderTop.addWidget(self.HeaderJsonVal, stretch = 5)
        self.DataRow.addLayout(self.HeaderTop)
        self.HeaderText = QTextEdit()
        self.HeaderText.textChanged.connect(self.UpdateOutput)
        self.DataRow.addWidget(self.HeaderText)

        self.PayloadTop = QHBoxLayout()
        self.PayloadLabel = QLabel("Payload: ")
        self.PayloadLabel.setObjectName("bold")
        self.PayloadTop.addWidget(self.PayloadLabel, stretch = 2)
        self.PayloadJsonVal = CreateValBox()
        self.PayloadTop.addWidget(self.PayloadJsonVal, stretch = 5)
        self.DataRow.addLayout(self.PayloadTop)
        self.PayloadText = QTextEdit()
        self.PayloadText.textChanged.connect(self.UpdateOutput)
        self.DataRow.addWidget(self.PayloadText)

        self.ProcessLayout.addLayout(self.DataRow)

        self.MainLayout.addLayout(self.ProcessLayout)

        self.MainLayout.addStretch()
    
    def ModeChanged(self, mode):
        self.Mode = mode
        if mode == "Decode":
            self.DecodeTab.setProperty("active", True)
            self.EncodeTab.setProperty("active", False)
            self.HeaderText.setReadOnly(True)
            self.PayloadText.setReadOnly(True)
            self.KeyText.setReadOnly(False)
            self.JWTtext.setReadOnly(False)
        elif mode == "Encode":
            self.DecodeTab.setProperty("active", False)
            self.EncodeTab.setProperty("active", True)
            self.HeaderText.setReadOnly(False)
            self.PayloadText.setReadOnly(False)
            self.KeyText.setReadOnly(True)
            self.JWTtext.setReadOnly(True)

        self.DecodeTab.style().unpolish(self.DecodeTab)
        self.EncodeTab.style().unpolish(self.EncodeTab)
        self.UpdateOutput()

    def UpdateOutput(self):
        if self.Mode == "Decode": self.DecodeJwt()
        else: self.EncodeJwt()
        self.RunValidation()
    
    def Encode(self, data, encoded = False):
        if not encoded:
            data = data.encode(self.ENCODING)
        return urlsafe_b64encode(data).decode(self.ENCODING).rstrip('=')

    def DecodeJwt(self):
        self.HeaderText.blockSignals(True)
        self.PayloadText.blockSignals(True)

        JWTstr = self.JWTtext.toPlainText().strip()
        JWTparts = JWTstr.split(".")
        try:
            self.HeaderText.setText("")
            HeaderB64 = JWTparts[0]
            HeaderJson = urlsafe_b64decode(HeaderB64 + "===").decode("utf-8")
            self.HeaderText.setText(HeaderJson)
            self.HeaderText.setText(json.dumps(json.loads(HeaderJson), indent=4))
        except:
            pass

        try:
            self.PayloadText.setText("")
            PayloadB64 = JWTparts[1]
            PayloadJson = urlsafe_b64decode(PayloadB64 + "===").decode("utf-8")
            self.PayloadText.setText(PayloadJson)
            self.PayloadText.setText(json.dumps(json.loads(PayloadJson), indent=4))
        except:
            pass
        
        self.HeaderText.blockSignals(False)
        self.PayloadText.blockSignals(False)
    
    def EncodeJwt(self):
        self.JWTtext.blockSignals(True)
        self.KeyText.blockSignals(True)

        try:
            Header = self.Encode(json.dumps(json.loads(self.HeaderText.toPlainText()), separators=(',', ':')))
            Payload = self.Encode(json.dumps(json.loads(self.PayloadText.toPlainText()), separators=(',', ':')))
            Signature = self.GenerateSignature([Header, Payload])
            self.JWTtext.setText(f"{Header}.{Payload}.{Signature}")
        except:
            Header = self.Encode(self.HeaderText.toPlainText())
            Payload = self.Encode(self.PayloadText.toPlainText())
            Signature = self.GenerateSignature([Header, Payload])
            self.JWTtext.setText(f"{Header}.{Payload}.{Signature}")

        self.JWTtext.blockSignals(False)
        self.KeyText.blockSignals(False)
    
    def GenerateSignature(self, JwtParts):
        key = self.KeyText.toPlainText().strip().encode(self.ENCODING)
        sig = ''

        try:
            Algo = self.HashFunc.currentText()
            data = JwtParts[0] + '.' + JwtParts[1]
            data = data.encode(self.ENCODING)
            HashFunc = self.HashAlgos[Algo]
            sig = self.Encode(hmac.new(key, data, HashFunc).digest(), encoded = True)
        except:
            pass

        return sig

    def RunValidation(self):
        tick = QPixmap(bk.ResourcePath("Images/tick.png")).scaled(20, 20)
        cross = QPixmap(bk.ResourcePath("Images/cross.png")).scaled(20, 20)
        JWTstr = self.JWTtext.toPlainText().strip()
        JWTparts = JWTstr.split(".")

        JwtValid = self.CheckJwtFormat(JWTparts)
        self.JWTval.setProperty("status", "success" if JwtValid else "fail")
        self.JWTval.text.setText(f"JWT format : {"valid" if JwtValid else "invalid"}")
        self.JWTval.icon.setPixmap(tick if JwtValid else cross)
        self.RefreshStyle(self.JWTval)

        HeaderValid = self.CheckHeaderFormat(JWTparts)
        self.HeaderBase64Val.setProperty("status", "success" if HeaderValid else "fail")
        self.HeaderBase64Val.text.setText(f"Header format : {"valid" if HeaderValid else "invalid"}")
        self.HeaderBase64Val.icon.setPixmap(tick if HeaderValid else cross)
        self.RefreshStyle(self.HeaderBase64Val)

        HeaderJson = self.CheckHeaderJson(JWTparts)
        self.HeaderJsonVal.setProperty("status", "success" if HeaderJson else "fail")
        self.HeaderJsonVal.text.setText(f"Header JSON : {"valid" if HeaderJson else "invalid"}")
        self.HeaderJsonVal.icon.setPixmap(tick if HeaderJson else cross)
        self.RefreshStyle(self.HeaderJsonVal)

        PayloadFormat = self.CheckPayloadFormat(JWTparts)
        self.PayloadBase64Val.setProperty("status", "success" if PayloadFormat else "fail")
        self.PayloadBase64Val.text.setText(f"Payload format : {"valid" if PayloadFormat else "invalid"}")
        self.PayloadBase64Val.icon.setPixmap(tick if PayloadFormat else cross)
        self.RefreshStyle(self.PayloadBase64Val)

        PayloadJson = self.CheckPayloadJson(JWTparts)
        self.PayloadJsonVal.setProperty("status", "success" if PayloadJson else "fail")
        self.PayloadJsonVal.text.setText(f"Payload JSON : {"valid" if PayloadJson else "invalid"}")
        self.PayloadJsonVal.icon.setPixmap(tick if PayloadJson else cross)
        self.RefreshStyle(self.PayloadJsonVal)

        KeyFormat = self.CheckKeyFormat()
        self.KeyFormatVal.setProperty("status", "success" if KeyFormat else "fail")
        self.KeyFormatVal.text.setText(f"Key format : {"valid" if KeyFormat else "invalid"}")
        self.KeyFormatVal.icon.setPixmap(tick if KeyFormat else cross)
        self.RefreshStyle(self.KeyFormatVal)

        ValidSign = self.CheckSignature(JWTparts)
        self.SignatureVal.setProperty("status", "success" if ValidSign else "fail")
        self.SignatureVal.text.setText(f"Signature validation : {"succeeded" if ValidSign else "failed"}")
        self.SignatureVal.icon.setPixmap(tick if ValidSign else cross)
        self.RefreshStyle(self.SignatureVal)
    
    def CheckJwtFormat(self, JwtParts):
        if len(JwtParts) == 3 and all(JwtParts):
            return True
        else:
            return False
    
    def CheckHeaderFormat(self, JwtParts):
        try:
            HeaderB64 = JwtParts[0]
            if not HeaderB64: raise Exception("Empty header")
            urlsafe_b64decode(HeaderB64 + "===").decode("utf-8")
            return True
        except:
            return False
    
    def CheckHeaderJson(self, JwtParts):
        try:
            HeaderB64 = JwtParts[0]
            if not HeaderB64: raise Exception("Empty header")
            HeaderJson = urlsafe_b64decode(HeaderB64 + "===").decode("utf-8")
            json.loads(HeaderJson)
            return True
        except:
            return False
    
    def CheckPayloadFormat(self, JwtParts):
        try:
            PayloadB64 = JwtParts[1]
            if not PayloadB64: raise Exception("Empty payload")
            urlsafe_b64decode(PayloadB64 + "===").decode("utf-8")
            return True
        except:
            return False
    
    def CheckPayloadJson(self, JwtParts):
        try:
            PayloadB64 = JwtParts[1]
            if not PayloadB64: raise Exception("Empty payload")
            PayloadJson = urlsafe_b64decode(PayloadB64 + "===").decode("utf-8")
            json.loads(PayloadJson)
            return True
        except:
            return False
    
    def CheckKeyFormat(self):
        try:
            key = self.KeyText.toPlainText().strip()
            if not key: raise Exception("Empty key")
            MinLen = int(self.HashFunc.currentText()[2:]) / 8
            if len(key) < MinLen:
                raise Exception("Key too short")
            
            return True
        except:
            return False
    
    def CheckSignature(self, JwtParts):
        try:
            key = self.KeyText.toPlainText().strip()
            sig = JwtParts[2].strip()
            if not key or not sig: raise Exception("Empty key or signature")

            ExpectedSig = self.GenerateSignature(JwtParts)
            if ExpectedSig != sig: raise Exception("Invalid signature")

            return True
        except:
            return False
    
    def RefreshStyle(self, widget):
        widget.style().unpolish(widget)
        widget.style().polish(widget)
        widget.update()
    
    def resizeEvent(self, event):
        ValBoxHeight = int(self.ValContainer.height() * 0.15)
        ValIconSize = int(ValBoxHeight * 0.8)
        for box in [self.JWTval, self.HeaderBase64Val, self.PayloadBase64Val, self.KeyFormatVal, self.SignatureVal, self.HeaderJsonVal, self.PayloadJsonVal]:
            box.setFixedHeight(ValBoxHeight)
            box.icon.setFixedSize(ValIconSize, ValIconSize)
        
        FontSiz = int(ValBoxHeight * 0.6)
        FontText = f'font-size: {FontSiz}px'
        self.JWTlabel.setStyleSheet(FontText)
        self.Keylabel.setStyleSheet(FontText)
        self.HashLabel.setStyleSheet(FontText)
        self.HeaderLabel.setStyleSheet(FontText)
        self.PayloadLabel.setStyleSheet(FontText)

        FontSiz = int(ValBoxHeight * 0.45)
        FontText = f'font-size: {FontSiz}px'
        self.PayloadBase64Val.text.setStyleSheet(FontText)
        self.HeaderBase64Val.text.setStyleSheet(FontText)
        self.PayloadJsonVal.text.setStyleSheet(FontText)
        self.HeaderJsonVal.text.setStyleSheet(FontText)
        self.SignatureVal.text.setStyleSheet(FontText)
        self.KeyFormatVal.text.setStyleSheet(FontText)
        self.JWTval.text.setStyleSheet(FontText)

        return super().resizeEvent(event)