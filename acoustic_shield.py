import subprocess
import argparse
import os

def apply_stealth_shield(input_file, output_file):
    print(f"[*] Deploying Advanced Stealth Shield on: {input_file}...")

    # The Advanced Filtergraph:
    # 1. [0:a] Strips real ENF, applies spectral denoise (afftdn), noise gate, and vibrato
    # 2. [noise] Generates continuous brown room-tone noise (c=brown)
    # 3. [fake_enf] Generates a synthetic decoy 60Hz sine wave (f=60)
    # 4. amix blends the three tracks together, matching the exact length of the original file (duration=first)
    
    filter_complex = (
        "[0:a]bandreject=f=60:width_type=h:w=2,bandreject=f=50:width_type=h:w=2,"
        "bandreject=f=120:width_type=h:w=2,afftdn=nf=-25,"
        "agate=threshold=-35dB:ratio=9000:range=-90dB,vibrato=f=0.4:d=0.008[shielded]; "
        "anoisesrc=a=0.015:c=brown[noise]; "
        "sine=f=60:a=0.005[fake_enf]; "
        "[shielded][noise][fake_enf]amix=inputs=3:duration=first[out_a]"
    )

    video_extensions = (".mp4", ".mov", ".mkv", ".avi", ".webm")
    is_video = input_file.lower().endswith(video_extensions)

    if is_video:
        # -map 0:v keeps the original video stream untouched
        # -map [out_a] attaches our newly generated stealth audio track
        command = [
            "ffmpeg", "-y", "-i", input_file, 
            "-filter_complex", filter_complex, 
            "-map", "0:v", "-map", "[out_a]", 
            "-c:v", "copy", 
            output_file
        ]
    else:
        command = [
            "ffmpeg", "-y", "-i", input_file, 
            "-filter_complex", filter_complex, 
            "-map", "[out_a]", 
            output_file
        ]

    try:
        subprocess.run(command, capture_output=True, text=True, check=True)
        print(f"[+] Stealth media exported successfully to: {output_file}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[!] FFmpeg processing error: {e.stderr}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advanced Acoustic Geolocation & Stealth ENF Countermeasure")
    parser.add_argument("-i", "--input", required=True, help="Path to raw input audio or video file")
    parser.add_argument("-o", "--output", default="stealth_output.wav", help="Path for sanitized output file")
    args = parser.parse_args()

    apply_stealth_shield(args.input, args.output)
