import os
from pypdf import PdfReader
from pptx import Presentation
from PIL import Image
import pytesseract

# WSL path targeting your Windows directory
directory = "/mnt/c/Users/Cortney H/Documents/CompTia Linux Notes"

# Open the universal staging file
with open("raw_extracted_notes.txt", "w") as output_file:
    
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        
        # 1. Handle PDFs
        if filename.endswith(".pdf"):
            print(f"Extracting PDF: {filename}...")
            reader = PdfReader(filepath)
            for page in reader.pages:
                raw_text = page.extract_text()
                if raw_text:
                    output_file.write(raw_text + "\n")
                    
        # 2. Handle PowerPoints
        elif filename.endswith(".pptx"):
            print(f"Extracting PPTX: {filename}...")
            prs = Presentation(filepath)
            for slide in prs.slides:
                for shape in slide.shapes:
                    # Check if the shape actually contains text before extracting
                    if hasattr(shape, "text"):
                        output_file.write(shape.text + "\n")
                        
        # 3. Handle Images via OCR
        elif filename.endswith(".png") or filename.endswith(".jpg"):
            print(f"Extracting Image OCR: {filename}...")
            img = Image.open(filepath)
            # Pass the Pillow image object to Tesseract
            raw_text = pytesseract.image_to_string()
            output_file.write(raw_text + "\n")

print("All files successfully scraped into raw_extracted_notes.txt.")
