from pydub import AudioSegment
from pydub.effects import normalize

# Load the tracks
print("Loading audio files...")
vocals = AudioSegment.from_file("raw_vocals.wav")
ambience = AudioSegment.from_file("ambient.wav")

# Normalize the vocals (flatten the dynamic range)
print("Normalizing vocals...")
processed_vocals = normalize(vocals)

# Drop the ambient volume by 15 decibels 
quiet_ambience = ambience - 15

# Loop the background track to match the vocal length
print("Syncing track durations...")
if len(quiet_ambience) < len(processed_vocals):
    loops_needed = (len(processed_vocals) // len(quiet_ambience)) + 1
    quiet_ambience = quiet_ambience * loops_needed

# Overlay the tracks
print("Mixing audio...")
final_mix = processed_vocals.overlay(quiet_ambience)

# Export the final polished track
print("Exporting final MP3...")
final_mix.export("final_podcast_episode.mp3", format="mp3")

print("Audio engineering complete. Track exported.")
