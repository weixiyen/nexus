import Image
import os
import collections
import re
from common import autocrop

def make_sprite(directory):
    directions = collections.defaultdict(list)

    max_width = 0
    max_height = 0

    for name in os.listdir(directory):
        if name.startswith('.'):
            continue

        _, desc = name[:-4].split('_')[1:]

        direction = re.sub('[^a-z]', '', desc)
        frame = re.sub('[a-z]', '', desc).lstrip('0')

        frame = int(frame) if frame else 0

        im = Image.open(os.path.join(directory, name))
        im = autocrop(im)

        max_width = max(max_width, im.size[0])
        max_height = max(max_height, im.size[1])

        directions[direction].append((frame, im))

    sprite = Image.new('RGBA', (max_width * len(directions['north']), max_height * len(directions)))

    meow = [
        'northwest', 'north', 'northeast',
        'west',
        'east',
        'southwest', 'south', 'southeast',
    ]

    for i, direction, in enumerate(meow):
        frames = directions[direction]

        for j, im in frames:
            left = max_width * j + ((max_width - im.size[0]) / 2)
            top = max_height * i + ((max_height - im.size[1]) / 2)

            sprite.paste(im, (left, top))

    sprite.save(directory + '.png')

make_sprite('robot')
make_sprite('ryu')
make_sprite('cray')
make_sprite('nina')