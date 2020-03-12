from PIL import Image

img = Image.new('RGBA', (200, 20), (0, 0, 0, 0))
pixel = img.load()
w, h = img.size
for x in range(w):
    for y in range(h):
        pixel[x, y] = (0, 0, 0, round((w - x - 1) / (w - 1) * 255))
img.save('newDa/value.png')
