import Image
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
