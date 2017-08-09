import common


def one_nbhd(img, width, height):
    img_processed = {}
    for y in range(0, height):
        for x in range(0, width):
            if x == 0 or x == width - 1 or y == 0 or y == height - 1:
                img_processed[x, y] = img[x, y]
            else:
                groups = {}
                for yt in range(y - 1, y + 2):
                    for xt in range(x - 1, x + 2):
                        dic_inc(groups, img[xt, yt])
                img_processed[x, y] = common.dic_key_max_count(groups)
    return img_processed


def img_to_partial(img, width, height, unknown_color, rnd_level):
    img_partial = {}
    for y in range(0, height):
        for x in range(0, width):
            if random.randint(1, rnd_level) == 1:
                img_partial[x, y] = img[x, y]
            else:
                img_partial[x, y] = unknown_color
    return img_partial
