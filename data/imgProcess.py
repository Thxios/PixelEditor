from PIL import Image


base_path = ''
todo = [
    'flood',
]

for target in todo:
    img = Image.open(base_path + target + '.png')
    img = img.convert('RGBA')

    pixel = img.load()
    wid, hei = img.size

    for global_x in range(wid):
        for global_y in range(hei):
            if pixel[global_x, global_y] == (0, 255, 0, 255):
                pixel[global_x, global_y] = (0, 0, 0, 0)

    img.save('processed_' + target + '.png')
