from PIL import Image

width = 256
height = 256

img = Image.new('RGB', (width, height), "black")
pixels = img.load()

for w in range(width):
    for h in range(height):
        pixels[w, h] = (int(w/width*255), int(h/height*255), 0)

img.show()