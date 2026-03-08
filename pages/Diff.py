import Backend as bk
import html
import difflib

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QPushButton, QLabel, QHBoxLayout, QFileDialog, QTextEdit

class DiffUtil(QWidget):
    def __init__(self):
        super().__init__()

        # Stylesheet
        self.setStyleSheet(bk.LoadStylesheet('DiffChecker'))

        self.ENCODING = 'utf-8'
        self.File1Text = ''
        self.File2Text = ''

        self.InitUI()
    
    def InitUI(self):
        self.MainLayout = QVBoxLayout(self)
        self.MainLayout.setContentsMargins(30, 30, 30, 30)
        self.MainLayout.setSpacing(20)

        # Header
        self.Header = QLabel("Diff Checker")
        self.Header.setObjectName("ToolTitle")
        self.Header.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.MainLayout.addWidget(self.Header)

        self.IOlayout = QHBoxLayout()

        self.File1Container = QWidget()
        self.File1Container.setObjectName("IOcont")
        self.File1Container.setContentsMargins(20, 0, 20, 0)
        self.File1Area = QVBoxLayout(self.File1Container)
        self.File1Area.addStretch(2)
        
        self.Input1Header = QLabel("Original File")
        self.Input1Header.setObjectName("SubHead")
        self.File1Area.addWidget(self.Input1Header, stretch=1)
        self.File1Area.addStretch(4)

        self.Inp1Lay = QHBoxLayout()
        self.Inp1Btn = QPushButton("Choose File")
        self.Inp1Btn.setObjectName("InpBtn")
        self.Inp1Btn.clicked.connect(lambda: self.OpenFile(True))
        self.Inp1Lay.addWidget(self.Inp1Btn, stretch=3)

        self.Fil1Label = QLabel("No file chosen")
        self.Fil1Label.setObjectName("FilLabel")
        self.Inp1Lay.addWidget(self.Fil1Label, stretch=5)
        self.Inp1Lay.addStretch(5)
        
        self.File1Area.addLayout(self.Inp1Lay, stretch=2)
        self.File1Area.addStretch(6)
        self.IOlayout.addWidget(self.File1Container, stretch=4)

        self.File2Container = QWidget()
        self.File2Container.setObjectName("IOcont")
        self.File2Container.setContentsMargins(20, 0, 20, 0)
        self.File2Area = QVBoxLayout(self.File2Container)
        self.File2Area.addStretch(2)
        
        self.Input2Header = QLabel("Modified File")
        self.Input2Header.setObjectName("SubHead")
        self.File2Area.addWidget(self.Input2Header, stretch=1)
        self.File2Area.addStretch(4)

        self.Inp2Lay = QHBoxLayout()
        self.Inp2Btn = QPushButton("Choose File")
        self.Inp2Btn.setObjectName("InpBtn")
        self.Inp2Btn.clicked.connect(lambda: self.OpenFile(False))
        self.Inp2Lay.addWidget(self.Inp2Btn, stretch=3)

        self.Fil2Label = QLabel("No file chosen")
        self.Fil2Label.setObjectName("FilLabel")
        self.Inp2Lay.addWidget(self.Fil2Label, stretch=5)
        self.Inp2Lay.addStretch(5)
        
        self.File2Area.addLayout(self.Inp2Lay, stretch=2)
        self.File2Area.addStretch(6)
        self.IOlayout.addWidget(self.File2Container, stretch=4)

        self.MainLayout.addLayout(self.IOlayout, stretch=4)

        self.PreviewLayout = QHBoxLayout()
        self.PreviewLayout.setSpacing(10)

        self.PreviewBox1 = QTextEdit()
        self.PreviewBox1.setObjectName("PreviewBox")
        self.PreviewBox1.setReadOnly(True)
        self.PreviewBox1.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap) 
        self.PreviewLayout.addWidget(self.PreviewBox1, stretch=1)

        self.PreviewBox2 = QTextEdit()
        self.PreviewBox2.setObjectName("PreviewBox")
        self.PreviewBox2.setReadOnly(True)
        self.PreviewBox2.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap) 
        self.PreviewLayout.addWidget(self.PreviewBox2, stretch=1)

        self.MainLayout.addLayout(self.PreviewLayout, stretch=9)
        self.MainLayout.addStretch(1)

        Vscroll1 = self.PreviewBox1.verticalScrollBar()
        Vscroll2 = self.PreviewBox2.verticalScrollBar()
        Vscroll1.valueChanged.connect(Vscroll2.setValue)
        Vscroll2.valueChanged.connect(Vscroll1.setValue)
        Hscroll1 = self.PreviewBox1.horizontalScrollBar()
        Hscroll2 = self.PreviewBox2.horizontalScrollBar()
        Hscroll1.valueChanged.connect(Hscroll2.setValue)
        Hscroll2.valueChanged.connect(Hscroll1.setValue)

    def OpenFile(self, Fil1):
        file, _ = QFileDialog.getOpenFileName(self, 'Open File')
        if not file: return
        try:
            with open(file, 'r', encoding=self.ENCODING) as fil: 
                if Fil1: self.File1Text = fil.read()
                else: self.File2Text = fil.read()
        except Exception:
            print("Invalid file data")
            return
        
        if Fil1: self.Fil1Label.setText(file.split('/')[-1])
        else: self.Fil2Label.setText(file.split('/')[-1])
        self.CompareFiles()

    def CompareFiles(self):
        if not self.File1Text and not self.File2Text:
            return
        
        lines1 = self.File1Text.splitlines()
        lines2 = self.File2Text.splitlines()

        matcher = difflib.SequenceMatcher(None, lines1, lines2)
        
        html1 = []
        html2 = []

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'equal':
                for line in lines1[i1:i2]:
                    html1.append(html.escape(line))
                    html2.append(html.escape(line))
            
            elif tag == 'replace':
                chunk1 = lines1[i1:i2]
                chunk2 = lines2[j1:j2]
                max_len = max(len(chunk1), len(chunk2))
                
                for idx in range(max_len):
                    if idx < len(chunk1):
                        html1.append(f'<span style="background-color: hsl(0, 70%, 25%); color: white;">{html.escape(chunk1[idx])}</span>')
                    else:
                        html1.append('')
                        
                    if idx < len(chunk2):
                        html2.append(f'<span style="background-color: hsl(120, 70%, 20%); color: white;">{html.escape(chunk2[idx])}</span>')
                    else:
                        html2.append('')

            elif tag == 'delete':
                for line in lines1[i1:i2]:
                    html1.append(f'<span style="background-color: hsl(0, 70%, 25%); color: white;">{html.escape(line)}</span>')
                    html2.append('')

            elif tag == 'insert':
                for line in lines2[j1:j2]:
                    html1.append('')
                    html2.append(f'<span style="background-color: hsl(120, 70%, 20%); color: white;">{html.escape(line)}</span>')

        self.PreviewBox1.setHtml(f"<pre>{'<br>'.join(html1)}</pre>")
        self.PreviewBox2.setHtml(f"<pre>{'<br>'.join(html2)}</pre>")