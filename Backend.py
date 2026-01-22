import sys
import os

tools = [
    "Case Converter", "Prettifier", "Encryption", "JWTs", "DateTime converter", "Colors", "Password Generator", 
    "QR/Barcode", ".md Preview", "Diff Checker", "Lorem Ipsum", "Unit converter"
]

def ResourcePath(RelPath):
    # Change path for pyinstaller shtuff
    try: Base = sys._MEIPASS
    except Exception: Base = os.path.abspath(".")
    path = os.path.join(Base, RelPath)
    return path if os.path.isfile(path) else None