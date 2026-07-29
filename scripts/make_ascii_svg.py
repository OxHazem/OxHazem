from PIL import Image

RAMP = " .`:-=+*cs#%@"
img = Image.open('source-prepped.png').convert('L').resize((100, 53))
pixels = img.load()
width, height = img.size

# Build the SVG with a typing animation
svg = '''

\n'''

for y in range(height):
    line = "".join([RAMP[int((255 - pixels[x, y]) / 255.0 * (len(RAMP) - 1))] for x in range(width)])
    safe_line = line.replace('&', '&').replace('<', '<').replace('>', '>')
    delay = y * 0.04
    svg += f'{safe_line}\n'

svg += ""

with open('avi-ascii.svg', 'w') as f:
    f.write(svg)
print("Success! Created avi-ascii.svg")