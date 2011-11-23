import Image
import os
import ImageChops
import ImageFilter

def autocrop(im):
    """
    Remove any unnecessary whitespace from the edges of the source image.

    This processor should be listed before :func:`scale_and_crop` so the
    whitespace is removed from the source image before it is resized.

    autocrop
        Activates the autocrop method for this image.

    """
    bw = im.convert('1')
    bw = bw.filter(ImageFilter.MedianFilter)
    # White background.
    bg = Image.new('1', im.size, 255)
    diff = ImageChops.difference(bw, bg)
    bbox = diff.getbbox()
    if bbox:
        im = im.crop(bbox)
    return im

directory = os.path.join(os.path.dirname(__file__), '../../public/img')

props = {
    'sprite_tree.png': ('prop/tree%d.png', 4, 1),
    'sprite_tower.png': ('structure/tower%d.png', 2, 1),
    'sprite_rock.png': ('prop/rock%d.png', 4, 1),
    'sprite_base.png': ('structure/base%d.png', 4, 2),
}

for fn, config in props.items():
    name, w_pieces, h_pieces = config

    image = Image.open(os.path.join(directory, fn))

    width, height = image.size

    box_w = width / w_pieces
    box_h = height / h_pieces

    for i in xrange(h_pieces):
        for j in xrange(w_pieces):
            box = ((box_w * j, box_h * i, box_w * (j + 1), box_h * (i + 1)))
            fn = os.path.join(directory, 'sprite', name % ((i + 1) * (j + 1)))
            print box
            slice = image.crop(box)
            slice = autocrop(slice)
            slice.save(fn)