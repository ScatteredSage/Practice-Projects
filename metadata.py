import os
import subprocess
import argparse

def extract_metadata(file_path):
    print("==========================================")
    print(f"Scanning {file_path} for hidden metadata...")
    print("==========================================")
    
    command = ["exiftool", file_path]
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error parsing file: {e}")
        return None

def scrub_metadata(file_path):
    print(f"[*] Scrubbing all metadata from {file_path}...")
    
    command = ["exiftool", "-all=", "-overwrite_original", file_path]
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print(f"[+] Successfully sanitized: {file_path} -> {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[!] Error scrubbing {file_path}: {e}")
        return False

# CLI Argument Orchestration
parser = argparse.ArgumentParser(description="Automated Metadata Forensics & Sanitizer (Images, Docs & Video)")
parser.add_argument("--scrub", action="store_true", help="Wipe all metadata headers in-place")
args = parser.parse_args()

target_directory = "."
# Expanded to include video containers (.mp4, .mov, .mkv) alongside images, docs, and audio
valid_extensions = (".jpg", ".jpeg", ".png", ".pdf", ".wav", ".mp3", ".mp4", ".mov", ".mkv")

for filename in os.listdir(target_directory):
    if filename.lower().endswith(valid_extensions):
        full_path = os.path.join(target_directory, filename)
        
        if args.scrub:
            scrub_metadata(full_path)
        else:
            metadata_results = extract_metadata(full_path)
            if metadata_results:
                print(metadata_results)
