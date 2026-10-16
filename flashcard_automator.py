import os
from pypdf import PdfReader 

# WSL path translation targeting your Windows C: drive
directory = "path_to_directory"

# Open a temporary text file to hold the raw scraped text
with open("raw_extracted_notes.txt", "w") as output_file:
    
    for filename in os.listdir(directory):
        # Ensure we only process PDF files
        if filename.endswith(".pdf"):
            filepath = os.path.join(directory, filename)
            
            # Terminal tracker so we know exactly which file it is working on
            print(f"Extracting: {filename}...")
            
            # Initialize the PDF reader on the current file
            reader = PdfReader(filepath)
            
            # Loop through every page in the current PDF
            for page in reader.pages:
                # Extract the raw text from the page
                raw_text = page.extract_text()
                
                # Write the text to our temporary file, adding a newline for spacing
                if raw_text:
                    output_file.write(raw_text + "\n")

print("All PDFs successfully scraped into raw text.")
