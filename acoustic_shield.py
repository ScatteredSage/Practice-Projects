import subprocess
import argparse
import os

def apply_acoustic_shield(input_file, output_file):
    print(f"[*] Deploying Acoustic & ENF Shield on: {input_file}...")

    # 1. The 3-Stage Defense Filter: ENF Grid Notch + Hard Noise Gate + Phase/Doppler Warp
    filter_chain = (
        "bandreject=f=60:width_type=h:w=2,"
        "bandreject=f=50:width_type=h:w=2,"
        "bandreject=f=120:width_type=h:w=2,"
        "agate=threshold=-35dB:ratio=9000:range=-90dB,"
        "vibrato=f=0.4:d=0.008"
    )

    # Detect if input is a video format based on extension
    video_extensions = (".mp4", ".mov", ".mkv", ".avi", ".webm")
    is_video = input_file.lower().endswith(video_extensions)

    if is_video:
        # For video: apply filter to audio (-af), copy video stream directly (-c:v copy) without re-encoding
        command = [
            "ffmpeg", "-y", "-i", input_file, 
            "-af", filter_chain, 
            "-c:v", "copy", 
            output_file
        ]
    else:
        # For standalone audio files
        command = [
            "ffmpeg", "-y", "-i", input_file, 
            "-af", filter_chain, 
            output_file
        ]

    try:
        subprocess.run(command, capture_output=True, text=True, check=True)
        print(f"[+] Shielded media exported successfully to: {output_file}")
        return True

    except subprocess.CalledProcessError as e:
        print(f"[!] FFmpeg processing error: {e.stderr}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Acoustic Geolocation & ENF Countermeasure Tool (Audio & Video)")
    parser.add_argument("-i", "--input", required=True, help="Path to raw input audio or video file")
    parser.add_argument("-o", "--output", default="shielded_output.wav", help="Path for sanitized output file")
    args = parser.parse_args()

    apply_acoustic_shield(args.input, args.output)
