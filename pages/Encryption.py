import Backend as bk
from os import urandom
from hashlib import md5, sha1, sha256, sha512, sha3_256, sha3_512
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from base64 import b64decode, b64encode
from pyperclip import copy

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QStackedWidget, QLineEdit, QSizePolicy, QComboBox, QTextEdit

class EncryptionUtil(QWidget):
    def __init__(self,):
        super().__init__()

        # Stylesheet
        self.setStyleSheet(bk.LoadStylesheet('Encryption'))

        self.Tabs = {}
        self.Mode = ''
        self.ENCODING = 'utf-8'

        self.InitUI()

        self.ModeChanged('Hashing')
    
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

        CreateTab("Hashing")
        CreateTab("AES")

        self.TabLayout.addStretch()
        self.MainLayout.addWidget(self.TabContainer)

        self.ProcessArea = QStackedWidget()

        self.HashingArea = self.HashingUI()
        self.ProcessArea.addWidget(self.HashingArea)
        self.AesArea = self.AesUI()
        self.ProcessArea.addWidget(self.AesArea)
        self.RsaArea = self.RsaUI()
        self.ProcessArea.addWidget(self.RsaArea)

        self.MainLayout.addWidget(self.ProcessArea, stretch=1)
    
    def HashingUI(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        def setup_row(text, InputName, BtnName, callback=None, readonly=False):
            RowLayout = QHBoxLayout()
            label = QLabel(text)
            label.setObjectName("lbl")
            
            input = QLineEdit()
            input.setReadOnly(readonly)
            input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            if callback: input.textEdited.connect(callback)
            setattr(self, InputName, input)
            
            copy = QPushButton()
            copy.setIcon(QIcon(bk.ResourcePath('Images/Clipboard.png')))
            copy.setObjectName("CopyBtn")
            copy.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            copy.clicked.connect(lambda: self.Copy(getattr(self, InputName)))
            setattr(self, BtnName, copy)
            
            RowLayout.addWidget(label)
            RowLayout.addWidget(input)
            RowLayout.addWidget(copy)
            
            layout.addLayout(RowLayout, stretch = 3)
            layout.addStretch(1)

        setup_row("Text:      ", "PlainTextInput", "PlainTextCopy", callback=lambda: self.UpdateHash('plain'))
        setup_row("Base64:    ", "Base64Input", "Base64Copy", callback=lambda: self.UpdateHash('b64'))
        setup_row("MD5:       ", "MD5Input", "MD5Copy", readonly=True)
        setup_row("SHA-1:     ", "SHA1Input", "SHA1Copy", readonly=True)
        setup_row("SHA-256:   ", "SHA256Input", "SHA256Copy", readonly=True)
        setup_row("SHA-512:   ", "SHA512Input", "SHA512Copy", readonly=True)
        setup_row("SHA-3 256: ", "SHA3_256Input", "SHA3_256Copy", readonly=True)
        setup_row("SHA-3 512: ", "SHA3_512Input", "SHA3_512Copy", readonly=True)

        return widget

    def AesUI(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        ConfRow = QHBoxLayout()
        ConfRow.addStretch(3)

        KeySizeLabel = QLabel("Key Size: ")
        ConfRow.addWidget(KeySizeLabel)
        KeySize = QComboBox()
        KeySize.addItems(['128', '192', '256'])
        ConfRow.addWidget(KeySize)
        ConfRow.addStretch(2)

        KeyFormatLabel = QLabel("Key Format: ")
        ConfRow.addWidget(KeyFormatLabel)
        KeyFormat = QComboBox()
        KeyFormat.addItems(['Hex', 'Base64', 'UTF-8'])
        ConfRow.addWidget(KeyFormat)
        ConfRow.addStretch(2)

        NonceFormatLabel = QLabel("Nonce Format: ")
        ConfRow.addWidget(NonceFormatLabel)
        NonceFormat = QComboBox()
        NonceFormat.addItems(['Hex', 'Base64', 'UTF-8'])
        ConfRow.addWidget(NonceFormat)
        ConfRow.addStretch(2)

        ConfRow.addStretch(3)
        layout.addLayout(ConfRow, stretch = 2)
        layout.addStretch(1)

        ConfRow2 = QHBoxLayout()
        ConfRow2.addStretch(3)

        PlaintextFormatLabel = QLabel("Plaintext Format: ")
        ConfRow2.addWidget(PlaintextFormatLabel)
        PlaintextFormat = QComboBox()
        PlaintextFormat.addItems(['Hex', 'Base64', 'UTF-8'])
        ConfRow2.addWidget(PlaintextFormat)
        ConfRow2.addStretch(2)

        CiphertextFormatLabel = QLabel("Ciphertext Format: ")
        ConfRow2.addWidget(CiphertextFormatLabel)
        CiphertextFormat = QComboBox()
        CiphertextFormat.addItems(['Hex', 'Base64', 'UTF-8'])
        ConfRow2.addWidget(CiphertextFormat)

        ConfRow2.addStretch(3)
        layout.addLayout(ConfRow2, stretch = 2)
        layout.addStretch(2)

        SecretRow = QHBoxLayout()

        KeyLabel = QLabel("Key:")
        KeyLabel.setObjectName("lbl")
        SecretRow.addWidget(KeyLabel)
        KeyInp = QLineEdit()
        KeyInp.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        SecretRow.addWidget(KeyInp)
        KeyGen = QPushButton()
        KeyGen.setIcon(QIcon(bk.ResourcePath('Images/Refresh.png')))
        KeyGen.setObjectName("GenBtn")
        KeyGen.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        KeyGen.clicked.connect(lambda: KeyInp.setText(self.RandomKey(int(KeySize.currentText()), KeyFormat.currentText())))
        SecretRow.addWidget(KeyGen)

        SecretRow.addSpacing(40)

        NonceLabel = QLabel("Nonce:")
        NonceLabel.setObjectName("lbl")
        SecretRow.addWidget(NonceLabel)
        NonceInp = QLineEdit()
        NonceInp.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        SecretRow.addWidget(NonceInp)
        NonceGen = QPushButton()
        NonceGen.setIcon(QIcon(bk.ResourcePath('Images/Refresh.png')))
        NonceGen.setObjectName("GenBtn")
        NonceGen.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        NonceGen.clicked.connect(lambda: NonceInp.setText(self.RandomNonce(NonceFormat.currentText())))
        SecretRow.addWidget(NonceGen)

        layout.addLayout(SecretRow, stretch = 1)
        layout.addStretch(1)

        OutLayout = QHBoxLayout()

        PlaintextLayout = QVBoxLayout()
        PlaintextLabel = QLabel("Plain Text: ")
        PlaintextLabel.setObjectName("lbl")
        PlaintextLayout.addWidget(PlaintextLabel, stretch = 1)
        Plaintext = QTextEdit()
        PlaintextLayout.addWidget(Plaintext, stretch = 5)
        OutLayout.addLayout(PlaintextLayout, stretch = 6)

        OutLayout.addStretch(1)

        CipherLayout = QVBoxLayout()
        CipherLabel = QLabel("Ciphertext: ")
        CipherLabel.setObjectName("lbl")
        CipherLayout.addWidget(CipherLabel, stretch = 1)
        Ciphertext = QTextEdit()
        CipherLayout.addWidget(Ciphertext, stretch = 5)
        OutLayout.addLayout(CipherLayout, stretch = 6)

        layout.addLayout(OutLayout, stretch = 10)
        layout.addStretch(1)

        GenBtn = QPushButton("Encrypt")
        GenBtn.setObjectName("MainBtn")
        GenBtn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        GenBtn.clicked.connect(lambda: self.AesEncrypt(KeySize.currentText(), KeyFormat.currentText(), NonceFormat.currentText(), 
                                                       PlaintextFormat.currentText(), CiphertextFormat.currentText(), 
                                                       KeyInp.text(), NonceInp.text(), Plaintext.toPlainText(), Ciphertext))
        layout.addWidget(GenBtn, alignment = Qt.AlignmentFlag.AlignCenter, stretch = 1)

        return widget
    
    def RsaUI(self):
        widget = QWidget()
        return widget
    
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
    
    def UpdateHash(self, source):
        text = b""
        try:
            if source == 'plain':
                text = self.PlainTextInput.text().encode(self.ENCODING)
                self.Base64Input.setText(b64encode(text).decode(self.ENCODING))
            elif source == 'b64':
                b64_val = self.Base64Input.text()
                text = b64decode((b64_val + '==').encode(self.ENCODING))
                self.PlainTextInput.setText(text.decode(self.ENCODING))
        except:
            return
        
        self.MD5Input.setText(md5(text).hexdigest())
        self.SHA1Input.setText(sha1(text).hexdigest())
        self.SHA256Input.setText(sha256(text).hexdigest())
        self.SHA512Input.setText(sha512(text).hexdigest())
        self.SHA3_256Input.setText(sha3_256(text).hexdigest())
        self.SHA3_512Input.setText(sha3_512(text).hexdigest())
    
    def RandomNonce(self, fmt):
        data = urandom(12)
        if fmt == 'Hex': return data.hex()
        elif fmt == 'Base64': return b64encode(data).decode(self.ENCODING)
        else: return data.decode(self.ENCODING, errors='replace')

    def RandomKey(self, length, fmt):
        data = urandom(length // 8)
        if fmt == 'Hex': return data.hex()
        elif fmt == 'Base64': return b64encode(data).decode(self.ENCODING)
        else: return data.decode(self.ENCODING, errors='replace')
    
    def AesEncrypt(self, KeySize, KeyFormat, NonceFormat, InpFormat, OutFormat, Key, Nonce, Inp, Out):
        try:
            def ToBytes(value, fmt):
                if not value: return b""
                if fmt == 'Hex':
                    sanitized = value.strip()
                    if len(sanitized) % 2 != 0:
                        sanitized = '0' + sanitized
                    return bytes.fromhex(sanitized)
                elif fmt == 'Base64':
                    return b64decode(value + '==')
                else:
                    return value.encode(self.ENCODING)

            def FromBytes(data, fmt):
                if fmt == 'Hex':
                    return data.hex()
                elif fmt == 'Base64':
                    return b64encode(data).decode(self.ENCODING)
                else:
                    return data.decode(self.ENCODING, errors='replace')

            KeyBytes = ToBytes(Key, KeyFormat)
            NonceBytes = ToBytes(Nonce, NonceFormat)
            InpBytes = ToBytes(Inp, InpFormat)

            TargetKeyLen = int(KeySize) // 8
            KeyBytes = KeyBytes.ljust(TargetKeyLen, b'\0')[:TargetKeyLen]

            TargetNonceLen = 12
            NonceBytes = NonceBytes.ljust(TargetNonceLen, b'\0')[:TargetNonceLen]

            self.AesArea.findChildren(QLineEdit)[0].setText(FromBytes(KeyBytes, KeyFormat))
            self.AesArea.findChildren(QLineEdit)[1].setText(FromBytes(NonceBytes, NonceFormat))

            aesgcm = AESGCM(KeyBytes)
            CipherBytes = aesgcm.encrypt(NonceBytes, InpBytes, None)

            Out.setText(FromBytes(CipherBytes, OutFormat))

        except Exception as e:
            Out.setText(f"Error: {str(e)}")
    
    def Copy(self, source):
        text = source.text()
        copy(text)
    
    def RefreshStyle(self, widget):
        widget.style().unpolish(widget)
        widget.style().polish(widget)
        widget.update()
    
    def resizeEvent(self, event):
        if self.ProcessArea.currentIndex() == 0:
            for btn in self.HashingArea.findChildren(QPushButton, "CopyBtn"):
                btn.setFixedWidth(btn.height())
                IconSiz = int(btn.height() * 0.5)
                btn.setIconSize(QSize(IconSiz, IconSiz))
            
            for label in self.HashingArea.findChildren(QLabel, "lbl"):
                FontSiz = int(label.height() * 0.4)
                label.setStyleSheet(f"font-size: {FontSiz}px")
        
        elif self.ProcessArea.currentIndex() == 1:
            for btn in self.AesArea.findChildren(QPushButton, "GenBtn"):
                btn.setFixedWidth(btn.height())
                IconSiz = int(btn.height() * 0.5)
                btn.setIconSize(QSize(IconSiz, IconSiz))

            for label in self.AesArea.findChildren(QLabel, "lbl"):
                FontSiz = int(label.height() * 0.5)
                label.setStyleSheet(f"font-size: {FontSiz}px")
            
            for btn in self.AesArea.findChildren(QPushButton, "MainBtn"):
                BtnFontSiz = int(btn.height() * 0.5)
                btn.setStyleSheet(f"font-size: {BtnFontSiz}px;")
        
            
        return super().resizeEvent(event)