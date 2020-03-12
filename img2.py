from PIL import Image

img = Image.open('newDa/hue4.png')
img = img.convert('RGBA')
pixel = img.load()
w, h = img.size
for x in range(w):
    for y in range(h):
        if pixel[x, y] != (0, 0, 0, 0):
            pixel[x, y] = (0, 0, 0, 255)

img.save('newDa/value_wheel.png')
