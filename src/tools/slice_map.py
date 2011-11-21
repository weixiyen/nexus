import Image
import os

directory = os.path.join(os.path.dirname(__file__), '../../public/img/map/')

image = Image.open('map.png')

width, height = image.size

pieces = 20

box_w = width / pieces
box_h = height / pieces

for i in xrange(pieces):
    for j in xrange(pieces):
        box = ((box_w * j, box_h * i, box_w * (j + 1), box_h * (i + 1)))
        print box
        slice = image.crop(box)
        slice.save(os.path.join(directory, '%d_%d.jpg' % (i, j)), 'JPEG', quality=90)