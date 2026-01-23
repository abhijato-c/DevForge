import sys
import os

tools = [
    "Case Converter", "Prettifier", "Encryption", "JWTs", "DateTime Converter", "Colors", "Password Generator", 
    "QR and Barcode", "Markdown", "Diff Checker", "Lorem Ipsum", "Unit Converter"
]

def ResourcePath(RelPath):
    # Change path for pyinstaller shtuff
    try: Base = sys._MEIPASS
    except Exception: Base = os.path.abspath(".")
    path = os.path.join(Base, RelPath)
    return path if os.path.isfile(path) else None

def LoadStylesheet(name):
    with open(ResourcePath('Styles/Global.css'), "r") as f:
        stylesheet = f.read()
    
    path = ResourcePath(f'Styles/{name}.css')
    if not path: return stylesheet
    with open(path, "r") as f:
        stylesheet += f.read()
    return stylesheet