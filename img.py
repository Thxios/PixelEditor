from PIL import Image

img = Image.open('newDa/hue.png')
img = img.convert('RGBA')
pixel = img.load()
w, h = img.size
for x in range(w):
    for y in range(h):
        if pixel[x, y] == (0, 0, 0, 255):
            pixel[x, y] = (0, 0, 0, 0)

img.thumbnail((201, 201))
img.save('newDa/hue3.png')
