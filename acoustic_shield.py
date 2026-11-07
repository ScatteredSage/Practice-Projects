import subprocess
import argparse

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

    # 2. Construct the full ffmpeg execution list
    command = ["ffmpeg", "-y", "-i", input_file, "-af", filter_chain, output_file]

    try:
        # 3. Execute the command list in an isolated child process
        subprocess.run(command, capture_output=True, text=True, check=True)
        print(f"[+] Shielded audio exported successfully to: {output_file}")
        return True

    except subprocess.CalledProcessError as e:
        print(f"[!] FFmpeg processing error: {e.stderr}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Acoustic Geolocation & ENF Countermeasure Tool")
    parser.add_argument("-i", "--input", required=True, help="Path to raw input audio file")
    parser.add_argument("-o", "--output", default="shielded_audio.wav", help="Path for sanitized output file")
    args = parser.parse_args()

    # 4. Route CLI arguments into the main function
    apply_acoustic_shield(args.input, args.output)
