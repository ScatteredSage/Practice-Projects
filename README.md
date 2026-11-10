# Practice-Projects: Python & Bash Utilities

A collection of Python and Bash utility scripts focused on cybersecurity automation, data parsing, and workflow optimization. 

## 🛠️ The Tools

### 1. The NLP Flashcard Pipeline

A two-stage pipeline that automates the conversion of unstructured study materials (PDFs, slide decks, and images) into strictly formatted Anki flashcards using the Gemini API.

*   **`ai_parser.py`**: The NLP engine. Reads the extracted text and passes it to the Gemini API with strict formatting instructions to generate Anki Cloze deletion flashcards (`Front | Extra`). Dynamically handles numbering to ensure a clean database import.

	**Non-technical breakdown**: A local API automation wrapper that routes raw text through Google's Gemini Flash AI model.

 	* **What it does: It takes unstructured text (like raw PDF extracts or presentation notes) and automatically uses AI to structure it into distinct Question/Answer pairs formatted cleanly for flashcards (Anki).

 	* **How to use it: To process a text file and output a cleaned file, type:
python3 ai_parser.py input.txt output.txt

*   **`flashcard_automator.py`**: The original, unified prototype script for the flashcard pipeline. It handles both basic PDF text extraction and Gemini API calls in a single execution, serving as the foundational logic before the system was upgraded into modular, multi-format stages.

	**Non-technical breakdown**: The final formatting engine for spaced-repetition studying.

 	* **What it does: It takes the AI-structured Question/Answer text and automatically builds a .csv file perfectly formatted for import into Anki (or Quizlet), saving hours of manual data entry.

 	* **How to use it: To generate your Anki deck, type:
python3 flashcard_automator.py parsed_data.txt flashcards.csv

*   **`universal_extractor.py`**: The data gatherer. Rips raw text from `.pdf`, `.pptx`, `.png`, and `.jpg` files using `pypdf`, `python-pptx`, and Tesseract OCR, standardizing the output into a single text file.

  	**Non-technical breakdown**: A multi-format document parser.

	* **​What it does: It automatically scans a folder and extracts the readable text from all your .pdf, .pptx, and .jpg/.png files (using Tesseract OCR for images) so the data is ready for the ai_parser.

 	* **How to use it: Simply place your documents in the target folder and type:
python3 universal_extractor.py

### 2. Automated Security Auditing

*   **`auto_scan.sh`**: A Bash wrapper script that automates system security audits by triggering `clamav`, `rkhunter`, and `lynis`, and parses the output for review.

	**Non-technical breakdown**: A Bash-scripted host enumeration utility.

 	* **What it does: It automatically scans the local machine, enumerating active ports, active users, and system information, compiling it into a timestamped security log.

 	* **How to use it: Make the script executable and run it:
chmod +x auto_scan.sh
./auto_scan.sh

*   **`Unified Detection Pipeline`**: A lightweight, Python-based Security Orchestration, Automation, and Response (SOAR) tool. This script monitors target log files in real-time, extracts Indicators of Compromise (IOCs) using regular expressions, and normalizes detected threats into JSON alert payloads mapped to actionable remediation playbooks.
	Features:
	*Dynamic Configuration: Switch environments (e.g., VPN, SSH) via CLI arguments without altering core logic.

	*Real-Time Ingestion: Tails log files efficiently without loading historical data into memory.

	*Synthetic Generator: Built-in test engine simulates network drops and brute-force attempts to validate extraction rules.

	*Usage:

	*Generate synthetic logs and test the pipeline:python3 pipeline.py --target vpn --test

	*Continuously monitor a live log file:python3 pipeline.py --target ssh

    **Non-technical breakdown**: 

	* **What it does: It acts like a mini-SIEM (Security Information and Event Management) tool. It continuously tails live system logs, extracts malicious IP addresses using regular expressions, formats alerts into JSON, and writes automated firewall block rules.
 
	​* **How to use it: To run a live security audit on a target log file, type:
python3 pipeline.py --log /var/log/syslog --mode analyze

	* **`metadata.py`: A bidirectional OSINT forensics extractor and metadata sanitizer utilizing Python's `os`, `subprocess`, and `argparse` modules to wrap `exiftool`. It supports images (`.jpg`, `.png`), documents (`.pdf`), audio (`.wav`, `.mp3`), and video containers (`.mp4`, `.mov`, `.mkv`). In audit mode, it extracts hidden EXIF, IPTC, XMP, and Composite headers. Passing `--scrub` executes an in-place sanitization pass (`-all= -overwrite_original`), stripping identifying metadata headers without leaving backup artifacts behind.

     **Non-technical breakdown**:
    
 	* **What it does: It can either read the hidden data (like exact location coordinates or device models) secretly attached to your photos, documents, and videos, or permanently wipe that hidden data to protect your privacy.

	* **How to use it (Audit Mode): To safely see what hidden data is currently on your files, type:
python3 metadata.py

	* **​How to use it (Sanitize Mode): To permanently wipe the hidden data from all files in the folder, type:
python3 metadata.py --scrub

* `acoustic_shield.py`: An advanced audio and video countermeasure utility built on `subprocess` and `ffmpeg` complex filtergraphs (`-filter_complex`) to neutralize Acoustic Geolocation (Aircraft Doppler Curve matching) and Electrical Network Frequency (ENF) power-grid analysis. It chains a triple-band notch filter (`bandreject` at 50Hz, 60Hz, and 120Hz), real-time spectral denoising (`afftdn` at `-25dB`), a hard digital noise gate (`agate` at `-35dB`), and a sub-perceptual pitch/phase modulator (`vibrato` at `0.4Hz`). To defeat forensic spectrogram inspection, it injects continuous analog room-tone (`anoisesrc` brown noise) and a synthetic `60Hz` decoy sine wave (`sine=f=60`). For video files (`.mp4`, `.mov`, `.mkv`), it maps the newly generated stealth audio track while copying the video stream directly (`-c:v copy`) without re-encoding visuals.
  
     **Non-technical breakdown**:An audio and video geolocation countermeasure.
 
* **What it does:** It isolates your voice, scrubs out continuous airplane background noise and power-grid hum in real-time, and injects a fake power-grid signal and warm microphone static so tracking algorithms fail and forensic analysts see what looks like normal, untampered audio.

 * **How to use it (Audio):** To protect an audio file, type: 
    `python3 acoustic_shield.py -i raw_vocals.wav -o stealth_audio.wav`
   
  * **How to use it (Video):** To protect the audio track of a video file (without changing the picture), type: 
    `python3 acoustic_shield.py -i raw_video.mp4 -o stealth_video.mp4`

### 3. Data Collection & Media

*   **`scraper.py`**: A Python web scraping utility designed to parse structured data from target web pages.

    **Non-technical breakdown**: A Python web scraping utility designed to parse structured data from target web pages.

	* **What it does: It automatically reads a website and extracts the specific text or data you want from it, saving you from having to copy and paste manually.

	* **How to use it: Type the command followed by the website you want to scan:
python3 scraper.py [https://example.com](https://example.com)

*   **`ascii_converter.py` & `ascii_animator.py`**: Python scripts utilizing the `Pillow` library to map image pixel brightness to ANSI characters, rendering full-color ASCII art and animations directly in the Linux terminal.

    **Non-technical breakdown**: Python scripts utilizing the Pillow library to map image pixel brightness to ANSI characters, rendering full-color ASCII art and animations directly in the Linux terminal.
 
	* **What it does: It converts normal pictures and videos into retro, text-based art (made entirely of keyboard characters and colors) that displays directly in your command line window.

	* **How to use it (Static Image): Type the command followed by your image file:
python3 ascii_converter.py image.png

	* **How to use it (Animation): Type the command followed by your video file:
python3 ascii_animator.py video.mp4

* `audio_engineer.py`: An automated audio mixing studio utilizing `pydub` and `ffmpeg`. It applies dynamic range compression to raw vocal tracks, attenuates background ambient tracks, calculates looping durations to match vocal length, and exports a leveled, broadcast-ready MP3. Supports an optional `--shield` flag that routes raw vocals through `acoustic_shield.py` prior to mixing.

    **Non-technical breakdown**: An automated podcast mixing studio.

	* **​What it does: It acts as a robot audio engineer. It automatically flattens your vocal volume, lowers the background music, matches the track lengths, and outputs a professional broadcast-ready MP3 file.

	* **Standard Usage:Ensure raw_vocals.wav and ambient.wav are in your folder, then type:
python3 audio_engineer.py`

	* **Privacy-Shielded Usage: To automatically run your vocals through the acoustic privacy shield before mixing the final track, type:
python3 audio_engineer.py --shield

*   **`reel_generator.py`**: A social media automation script utilizing `moviepy` and Pillow. It stretches a static thematic artwork `.png` to match the exact duration of an engineered audio track, formats it into a 1080x1920 vertical container, and exports a broadcast-ready `.mp4` video optimized for Instagram Reels and YouTube Shorts.

    **Non-technical breakdown**: 

	* **What it does: It takes your final podcast audio and a background picture, combines them, formats the size perfectly for vertical phone screens, and outputs a finished video ready to upload.

	* **How to use it: Ensure your completed audio and image files are in the folder, then type:
python3 reel_generator.py

## ⚙️ Installation & Setup

These scripts require Python 3 and several external libraries. It is recommended to run them within an isolated virtual environment (`venv`).

**1. Clone the repository**
```bash
git clone [https://github.com/ScatteredSage/Practice-Projects.git](https://github.com/ScatteredSage/Practice-Projects.git)
cd Practice-Projects
