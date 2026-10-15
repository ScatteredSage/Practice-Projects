import sys
from PIL import Image, ImageEnhance
from fpdf import FPDF

# Ensure the user provides an image file when running the script
if len(sys.argv) < 2:
    print("Usage: python ascii_converter.py <path_to_image.jpg>")
    sys.exit()

image_path = sys.argv[1]
print(f"Processing target: {image_path}")

# 1. Load and enhance the original image
try:
    img = Image.open(image_path).convert('RGB')
except FileNotFoundError:
    print("Error: Image file not found.")
    sys.exit()

# Boost contrast and saturation
img = ImageEnhance.Color(img).enhance(1.2)
img = ImageEnhance.Contrast(img).enhance(1.1)

# Scale resolution
width = 130
height = int(width * img.height / img.width * 0.53)
img = img.resize((width, height), Image.Resampling.LANCZOS)

# 2. Initialize PDF Canvas
pdf = FPDF(orientation='P', unit='mm', format='A4')
pdf.add_page()
pdf.set_fill_color(10, 10, 15)
pdf.rect(0, 0, 210, 297, 'F')
pdf.set_font('Courier', size=3.5)

# High-detail character map
ascii_chars = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,"^`\'. '

# 3. Render the artwork row by row
pdf.set_y(10)
for y in range(height):
    pdf.set_x(10)
    for x in range(width):
        r, g, b = img.getpixel((x, y))
        
        # Calculate perceived brightness
        brightness = int(0.299*r + 0.587*g + 0.114*b)
        char_idx = int((brightness / 256) * len(ascii_chars))
        char = ascii_chars[min(char_idx, len(ascii_chars)-1)]
        
        # Draw the character in color
        pdf.set_text_color(max(r, 40), max(g, 40), max(b, 40))
        pdf.cell(1.4, 1.4, txt=char, border=0, ln=0, align='C')
    pdf.ln(1.6)

# Save the final file
output_name = "vivid_art_output.pdf"
pdf.output(output_name)
print(f"Success! Artwork saved as {output_name}")
