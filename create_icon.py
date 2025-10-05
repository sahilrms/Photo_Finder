from PIL import Image, ImageDraw, ImageFont
import os

# Create a 256x256 image with a blue background
img = Image.new('RGBA', (256, 256), (66, 165, 245, 255))
draw = ImageDraw.Draw(img)

# Try to load a font, fall back to default if not available
try:
    font = ImageFont.truetype("arial.ttf", 100)
except IOError:
    font = ImageFont.load_default()

# Draw a simple camera icon
draw.ellipse((30, 30, 226, 226), outline='white', width=10)
draw.ellipse((60, 60, 196, 196), fill='white')
draw.ellipse((90, 90, 166, 166), fill=(66, 165, 245))

# Save the icon
img.save('app_icon.ico', format='ICO', sizes=[(256, 256)])
print("Icon created: app_icon.ico")
