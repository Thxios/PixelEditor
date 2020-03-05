import numpy as np
from PIL import Image

a = np.zeros((100, 150, 4), dtype=np.uint8)
len(a)
a[:, :, :] = [0, 0, 0, 255]
a[10:, :, :] = [255, 128, 0, 255]

img = Image.fromarray(a, 'RGBA')
img.save('temp.png')
