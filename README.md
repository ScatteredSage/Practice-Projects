# Practice-Projects: Python & Bash Utilities

A collection of Python and Bash utility scripts focused on cybersecurity automation, data parsing, and workflow optimization. 

## 🛠️ The Tools

### 1. The NLP Flashcard Pipeline
A two-stage pipeline that automates the conversion of unstructured study materials (PDFs, slide decks, and images) into strictly formatted Anki flashcards using the Gemini API.

*   **`universal_extractor.py`**: The data gatherer. Rips raw text from `.pdf`, `.pptx`, `.png`, and `.jpg` files using `pypdf`, `python-pptx`, and Tesseract OCR, standardizing the output into a single text file.
*   **`ai_parser.py`**: The NLP engine. Reads the extracted text and passes it to the Gemini API with strict formatting instructions to generate Anki Cloze deletion flashcards (`Front | Extra`). Dynamically handles numbering to ensure a clean database import.

### 2. Automated Security Auditing
*   **`auto_scan.sh`**: A Bash wrapper script that automates system security audits by triggering `clamav`, `rkhunter`, and `lynis`, and parses the output for review.

### 3. Data Collection & Media
*   **`scraper.py`**: A Python web scraping utility designed to parse structured data from target web pages.
*   **`ascii_converter.py` & `ascii_animator.py`**: Python scripts utilizing the `Pillow` library to map image pixel brightness to ANSI characters, rendering full-color ASCII art and animations directly in the Linux terminal.

## ⚙️ Installation & Setup

These scripts require Python 3 and several external libraries. It is recommended to run them within an isolated virtual environment (`venv`).

**1. Clone the repository**
```bash
git clone [https://github.com/ScatteredSage/Practice-Projects.git](https://github.com/ScatteredSage/Practice-Projects.git)
cd Practice-Projects
