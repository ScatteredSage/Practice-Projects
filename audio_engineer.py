import os
import argparse
from pydub import AudioSegment, effects
from acoustic_shield import apply_acoustic_shield

def engineer_audio(vocal_path="raw_vocals.wav", ambient_path="ambient.wav", output_path="final_podcast_episode.mp3", use_shield=False):
    active_vocal_file = vocal_path

    # Optional Pre-Processing: Acoustic & ENF Countermeasure
    if use_shield:
        shielded_temp = "temp_shielded_vocals.wav"
        if apply_acoustic_shield(vocal_path, shielded_temp):
            active_vocal_file = shielded_temp

    print(f"[*] Loading audio tracks: {active_vocal_file} & {ambient_path}...")
    vocals = AudioSegment.from_wav(active_vocal_file)
    ambient = AudioSegment.from_wav(ambient_path)

    print("[*] Applying dynamic range compression and normalization to vocals...")
    vocals = effects.normalize(vocals)
    vocals = effects.compress_dynamic_range(vocals, threshold=-20.0, ratio=4.0, attack=5.0, release=50.0)
    vocals = effects.normalize(vocals)

    print("[*] Attenuating ambient track and matching vocal duration...")
    ambient = ambient - 14
    target_duration = len(vocals)
    
    if len(ambient) < target_duration:
        loops = (target_duration // len(ambient)) + 1
        ambient = ambient * loops
    ambient = ambient[:target_duration]

    print("[*] Mixing tracks and exporting broadcast-ready MP3...")
    final_mix = vocals.overlay(ambient)
    final_mix.export(output_path, format="mp3", bitrate="192k")
    print(f"[+] Export complete: {output_path}")

    # Clean up temporary shielded WAV artifact
    if use_shield and os.path.exists("temp_shielded_vocals.wav"):
        os.remove("temp_shielded_vocals.wav")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automated Audio Mixing Studio")
    parser.add_argument("--shield", action="store_true", help="Apply Acoustic Geolocation & ENF Shield to vocals before mixing")
    args = parser.parse_args()

    engineer_audio(use_shield=args.shield)
