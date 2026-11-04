import os
import subprocess

def extract_metadata(file_path):
    print("==========================================")
    print(f"Scanning {file_path} for hidden metadata...")
    print("==========================================")
    
    command = ["exiftool", file_path]
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        raw_metadata = result.stdout
        return raw_metadata
        
    except subprocess.CalledProcessError as e:
        print(f"Error parsing file: {e}")
        return None

# Automated Directory Scanner
target_directory = "."
valid_extensions = (".jpg", ".jpeg", ".png", ".pdf", ".wav", ".mp3")

for filename in os.listdir(target_directory):
    if filename.lower().endswith(valid_extensions):
        full_path = os.path.join(target_directory, filename)
        metadata_results = extract_metadata(full_path)
        
        if metadata_results:
            print(metadata_results)
