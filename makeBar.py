from PIL import Image

img = Image.open('newDa/alpha2.png')
img = img.convert('RGBA')
pixel = img.load()
w, h = img.size
for x in range(w):
    for y in range(h):
        _r, _g, _b, _ = pixel[x, y]
        pixel[x, y] = (_r, _g, _b, round((w - x - 1) / (w - 1) * 255))
img.save('newDa/alpha_bar.png')
