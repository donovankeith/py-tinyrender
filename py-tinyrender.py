# Imports
from PIL import Image
from math import floor

# Image Size
image_width = 256
image_height = 256

image = Image.new('RGB', (image_width, image_height), "black")
pixels = image.load()

# Preset colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Assign colors
pixels[100, 100] = red

def line(x0, y0, x1, y1, pixels, color): 
    steps = 1000
    
    for step in range(steps):
        t = step/steps

        x = x0 + (x1-x0) * t
        y = y0 + (y1-y0) * t

        pixels[int(x), int(y)] = color

line(10, 10, 255, 255, pixels, red)

# Flip Top/Bottom so that drawing is done in more intuitive directions.
image.transpose(Image.FLIP_LEFT_RIGHT)

image.show()
