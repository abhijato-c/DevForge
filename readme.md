# DevForge Utilities

**DevForge** is a centralized, cross-platform desktop suite designed to streamline the daily workflow of developers. Built with Python and PyQt6, it eliminates the need for dozens of open browser tabs by providing essential conversion, formatting, and generation tools in a single interface.

NOTE: Only certain programming languages supported in case converter and prettifier.

---

## Features

The application features a responsive dashboard and a sidebar for quick navigation between the following utilities:

* **Case Converter:** Quickly toggle between `camelCase`, `snake_case`, `PascalCase`, and more.
* **Prettifier:** Format and beautify messy code or data structures.
* **Encryption:** Secure data using modern encryption standards (like AES-GCM).
* **JWT Debugger:** Decode and inspect JSON Web Tokens on the fly.
* **DateTime Converter:** Seamlessly switch between Unix timestamps and human-readable dates.
* **Password Generator:** Create secure, cryptographically strong passwords with custom constraints.
* **Diff Checker:** Compare two blocks of text to identify structural or content differences.
* **Lorem Ipsum:** Generate placeholder text for UI/UX prototyping.

---

## Project Structure

```text
DevForge/
├── main.py              # Entry point & Window Management
├── Backend.py           # Logic for resource handling & Stylesheet loading
├── Home.py              # Responsive Dashboard/Grid UI
├── pages/               # Individual tool implementations (CaseUtil, EncryptionUtil, etc.)
├── Styles/              # QSS files for global and page-specific styling
└── Images/              # UI Icons and assets

```

---

## Cloning and editing

1. **Clone the repository:**
```bash
git clone https://github.com/your-username/DevForge.git
cd DevForge

```


2. **Install dependencies:**
```bash
pip install -r requirements.txt

```


3. **Run the application:**
```bash
python main.py

```