import Backend as bk
import autopep8, jsbeautifier, json, sqlparse, xml.dom.minidom

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QPushButton, QLabel, QHBoxLayout, QFileDialog, QTextEdit

class PrettifyUtil(QWidget):
    def __init__(self):
        super().__init__()

        # Stylesheet
        self.setStyleSheet(bk.LoadStylesheet('Prettifier'))

        self.ENCODING = 'utf-8'
        self.File = ''
        self.Output = ''

        self.InitUI()
    
    def InitUI(self):
        self.MainLayout = QVBoxLayout(self)
        self.MainLayout.setContentsMargins(30, 30, 30, 30)
        self.MainLayout.setSpacing(20)

        # Header
        self.Header = QLabel("Prettifier")
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
        self.InputArea.addStretch(4)

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
        self.InputArea.addStretch(3)
        self.IOlayout.addWidget(self.InputContainer, stretch = 4)

        self.OutputContainer = QWidget()
        self.OutputContainer.setContentsMargins(20, 0, 20, 0)
        self.OutputContainer.setObjectName("IOcont")
        self.OutputArea = QVBoxLayout(self.OutputContainer)
        self.OutputArea.addStretch(2)

        self.OutputLabel = QLabel("Output: ")
        self.OutputLabel.setObjectName("SubHead")
        self.OutputArea.addWidget(self.OutputLabel, stretch = 1)
        self.OutputArea.addStretch(4)

        self.DownloadBtn = QPushButton("Download")
        self.DownloadBtn.setObjectName("DownBtn")
        self.DownloadBtn.clicked.connect(self.DownloadResult)
        self.DownloadBtn.setEnabled(False)
        self.OutputArea.addWidget(self.DownloadBtn, stretch = 1)
        self.OutputArea.addStretch(3)
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
        ext = file.split('.')[-1]

        if ext in ['py', 'pyw']:
            self.Output = autopep8.fix_code(self.File)
            
        elif ext in ['js', 'html', 'htm', 'css']:
            self.Output = jsbeautifier.beautify(self.File)
        
        elif ext == 'json':
            self.Output = json.dumps(json.loads(self.File), indent=4)
        
        elif ext == 'sql':
            self.Output = sqlparse.format(self.File, reindent=True, keyword_case='upper')
        
        elif ext == 'xml':
            dom = xml.dom.minidom.parseString(self.File)
            self.Output = dom.toprettyxml(indent="    ")

        else:
            self.Output = "Unsupported file format"

        if self.Output: self.DownloadBtn.setEnabled(True)
        self.PreviewBox.setText(self.Output)
    
    def DownloadResult(self):
        file, _ = QFileDialog.getSaveFileName(self, 'Save File')
        if file:
            with open(file, 'w') as file:
                file.write(self.Output)