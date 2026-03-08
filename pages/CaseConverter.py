import Backend as bk
from caseconverter import pascalcase, camelcase, snakecase, kebabcase
from pygments import lexers, token, util
import re
import html

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QPushButton, QLabel, QHBoxLayout, QFileDialog, QComboBox, QTextEdit

class CaseUtil(QWidget):
    def __init__(self):
        super().__init__()

        # Stylesheet
        self.setStyleSheet(bk.LoadStylesheet('CaseConverter'))

        self.ENCODING = 'utf-8'
        self.File = ''
        self.Output = ''
        self.Converters = {
            'snake_case' : snakecase,
            'kebab-case' : kebabcase, 
            'camelCase' : camelcase, 
            'PascalCase' : pascalcase
        }

        self.InitUI()
    
    def InitUI(self):
        self.MainLayout = QVBoxLayout(self)
        self.MainLayout.setContentsMargins(30, 30, 30, 30)
        self.MainLayout.setSpacing(20)

        # Header
        self.Header = QLabel("Case Converter")
        self.Header.setObjectName("ToolTitle")
        self.Header.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.MainLayout.addWidget(self.Header)

        self.IOlayout = QHBoxLayout()

        self.InputContainer = QWidget()
        self.InputContainer.setObjectName("IOcont")
        self.InputContainer.setContentsMargins(20, 0, 0, 0)
        self.InputArea = QVBoxLayout(self.InputContainer)
        self.InputArea.addStretch(2)
        self.InputHeader = QLabel("Input File")
        self.InputHeader.setObjectName("SubHead")
        self.InputArea.addWidget(self.InputHeader, stretch = 1)
        self.InputArea.addStretch(6)

        self.InpLay = QHBoxLayout()
        self.InpBtn = QPushButton("Choose File")
        self.InpBtn.setObjectName("InpBtn")
        self.InpBtn.clicked.connect(self.OpenFile)
        self.InpLay.addWidget(self.InpBtn, stretch = 3)

        self.FilLabel = QLabel("No file chosen")
        self.FilLabel.setObjectName("FilLabel")
        self.InpLay.addWidget(self.FilLabel, stretch = 5)
        self.InpLay.addStretch(5)
        self.InputArea.addLayout(self.InpLay, stretch = 2)
        self.InputArea.addStretch(2)

        self.ModeLay = QHBoxLayout()
        self.ModeLabel = QLabel("Choose case: ")
        self.ModeLabel.setObjectName("ModeLabel")
        self.ModeLay.addWidget(self.ModeLabel, stretch = 3)
        self.ModeSel = QComboBox()
        self.ModeSel.addItems(['snake_case', 'kebab-case', 'camelCase', 'PascalCase'])
        self.ModeLay.addWidget(self.ModeSel, stretch = 5)
        self.ModeLay.addStretch(10)
        self.InputArea.addLayout(self.ModeLay)
        self.InputArea.addStretch(6)
        self.IOlayout.addWidget(self.InputContainer, stretch = 4)

        self.OutputContainer = QWidget()
        self.OutputContainer.setContentsMargins(20, 0, 20, 0)
        self.OutputContainer.setObjectName("IOcont")
        self.OutputArea = QVBoxLayout(self.OutputContainer)
        self.OutputArea.addStretch(1)

        self.OutputLabel = QLabel("Output: ")
        self.OutputLabel.setObjectName("SubHead")
        self.OutputArea.addWidget(self.OutputLabel, stretch = 1)
        self.OutputArea.addStretch(3)

        self.DownloadBtn = QPushButton("Download")
        self.DownloadBtn.setObjectName("DownBtn")
        self.DownloadBtn.clicked.connect(self.DownloadResult)
        self.DownloadBtn.setEnabled(False)
        self.OutputArea.addWidget(self.DownloadBtn, stretch = 1)
        self.OutputArea.addStretch(5)
        self.IOlayout.addWidget(self.OutputContainer, stretch = 4)
        self.MainLayout.addLayout(self.IOlayout, stretch = 4)

        self.PreviewBox = QTextEdit()
        self.PreviewBox.setObjectName("PreviewBox")
        self.PreviewBox.setReadOnly(True)
        self.PreviewBox.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap) 
        self.MainLayout.addWidget(self.PreviewBox, stretch = 9)

        self.MainLayout.addStretch(1)

    def OpenFile(self):
        file, _ = QFileDialog.getOpenFileName(self, 'Open File')
        if not file: return

        try:
            with open(file, 'r', encoding = self.ENCODING) as fil: self.File = fil.read()
        except:
            print("Invalid file data")
            return
        
        self.FilLabel.setText(file.split('/')[-1])

        replace = re.findall(r'\b(?:def|class|var|let|function|const)\s+([a-zA-Z_][a-zA-Z0-9_]*)', self.File)
        replace += re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*=', self.File)
        replace += re.findall(r'\.([a-zA-Z_][a-zA-Z0-9_]*)\s*=', self.File)
        
        replace = set(replace)
        replace.discard('self')

        try:
            lexer = lexers.get_lexer_for_filename(file)
        except util.ClassNotFound:
            print(f"Error: Invalid programming language")
            return
        
        tokens = lexer.get_tokens(self.File)
        Converter = self.Converters[self.ModeSel.currentText()]
        result = []
        PrevList = []

        for typ, value in tokens:
            if typ in token.Name and value in replace:
                converted = Converter(value)
                result.append(converted)
                
                if converted != value:
                    PrevList.append(f'<span style="background-color: hsl(220, 90%, 40%); color: white; font-weight: bold;">{html.escape(converted)}</span>')
                else:
                    PrevList.append(html.escape(converted))
            else:
                result.append(value)
                PrevList.append(html.escape(value))
        
        self.Output = "".join(result)
        if self.Output: self.DownloadBtn.setEnabled(True)

        self.PreviewBox.setHtml(f"<pre>{''.join(PrevList)}</pre>")
    
    def DownloadResult(self):
        file, _ = QFileDialog.getSaveFileName(self, 'Save File')
        if file:
            with open(file, 'w') as file:
                file.write(self.Output)