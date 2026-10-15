import sys
import time
from PIL import Image

# Ensure the user provides a GIF file
if len(sys.argv) < 2:
    print("Usage: python ascii_animator.py <path_to_gif>")
    sys.exit()

gif_path = sys.argv[1]

try:
    img = Image.open(gif_path)
except FileNotFoundError:
    print("Error: GIF not found.")
    sys.exit()

# Terminal dimensions
width = 42
aspect_ratio = 0.45 

ascii_chars = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,"^`\'. '
frames = []

print("Extracting frames and processing colors... hold tight.")

# Loop through every frame in the GIF
try:
    while True:
        # Convert frame to RGB to capture colors
        frame = img.convert("RGB")
        height = int(width * frame.height / frame.width * aspect_ratio)
        frame = frame.resize((width, height), Image.Resampling.NEAREST)
        
        ascii_frame = ""
        for y in range(height):
            for x in range(width):
                r, g, b = frame.getpixel((x, y))
                
                brightness = int(0.299*r + 0.587*g + 0.114*b)
                
                # The Transparency Threshold
                if brightness < 25:
                    char = " "
                else:
                    char_idx = int((brightness / 256) * len(ascii_chars))
                    char = ascii_chars[min(char_idx, len(ascii_chars)-1)]

                
                # Apply ANSI escape code for precise RGB coloring in the terminal
                ascii_frame += f"\033[38;2;{r};{g};{b}m{char}\033[0m"
            ascii_frame += "\n"
            
        frames.append(ascii_frame)
        # Move to the next frame in the GIF
        img.seek(img.tell() + 1)
except EOFError:
    pass # Reached the end of the GIF

# Clear the screen once before starting the loop
sys.stdout.write("\033[2J")

# The playback loop
try:
    for _ in range(1): # This plays the GIF exactly 1 times
        for frame in frames:
            # Move cursor to the top left (prevents screen flicker)
            sys.stdout.write("\033[H")
            sys.stdout.write(frame)
            sys.stdout.flush()
            time.sleep(0.12) # Frame speed (lower is faster)
except KeyboardInterrupt:
    # Reset terminal colors when you press Ctrl+C to exit
    sys.stdout.write("\033[0m\nAnimation stopped.\n")
