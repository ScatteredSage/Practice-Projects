from PIL import Image
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

from moviepy.editor import AudioFileClip, ImageClip

print("Loading media assets...")
# Load the mastered audio from your audio_engineer script
audio_track = AudioFileClip("final_podcast_episode.mp3")

# Load the thematic artwork (e.g., your "Struggle" or "Success" palette composition)
visual_theme = ImageClip("thematic_artwork.png")

print("Synchronizing visual duration to audio length...")
# Stretch the single image to match the exact length of the audio track
video_clip = visual_theme.set_duration(audio_track.duration)

# Attach the audio track to the video container
video_clip = video_clip.set_audio(audio_track)

# Resize to standard 1080x1920 vertical format for Reels/Shorts/TikTok
# Note: Ensure your original art is drawn in a 9:16 aspect ratio so it doesn't stretch weirdly
print("Formatting for vertical social media...")
video_clip = video_clip.resize(height=1920, width=1080)

print("Encoding final MP4 video... (This may take a few minutes)")
# Export the final file at 24 frames per second
video_clip.write_videofile("social_media_reel.mp4", fps=24, codec="libx264", audio_codec="aac")

print("Video rendering complete. Ready for upload.")
