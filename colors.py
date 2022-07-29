import numpy as np
from tqdm import tqdm
from PIL import Image
import matplotlib
import matplotlib.pyplot as plt
import random


from collections import deque as queue


def is_valid(array, seen, point):
    if point in seen:
        return False

    y, x = point
    ymax, xmax = array.shape
    in_bounds = (0 <= x < xmax) and (0 <= y < ymax)
    if not in_bounds:
        return False

    is_white = array[y, x] == 255
    if not is_white:
        return False

    return True


def get_neighbors(center):
    x, y = center
    return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]


def bfs(array, seen, source):
    y_coords = []
    x_coords = []
    if not is_valid(array, seen, source):
        return y_coords, x_coords
    q = queue()
    q.append(source)
    seen.add(source)
    while q:
        center = q.popleft()
        y_coords.append(center[0])  # remember numpy indexing is flipped!
        x_coords.append(center[1])
        neighbors = get_neighbors(center)
        for neighbor in neighbors:
            if is_valid(array, seen, neighbor):
                seen.add(neighbor)
                q.append(neighbor)
    return y_coords, x_coords


def main():
    # img = Image.open("data/gates_of_hell_clean.png")
    img = Image.open("outputs/eroded_gates_radius2.png")

    # preprocessing
    a = np.array(img)
    a[a < 255 // 2] = 0  # black pixels
    a[a >= 255 // 2] = 255  # white pixels

    # matrix b stores RGB values, so we have to add a dimension (matrix a stores binary for black/white)
    new_shape = list(a.shape) + [3]
    b = np.repeat(a, 3).reshape(new_shape).astype(int)

    # find the contiguous white regions in the picture
    explored = set()

    for source in tqdm(list(zip(*np.where(a == 255)))):  # look for white pixels
        x_coords, y_coords = bfs(a, explored, source)
        b[x_coords, y_coords] = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]

    # to matplotlib
    # dpi = matplotlib.rcParams['figure.dpi']
    # height, width = a.shape
    # figsize = (width / float(dpi), height / float(dpi))
    # plt.figure(figsize=figsize)
    # plt.imshow(b)
    # plt.show()

    output = Image.fromarray(b[...,::-1].astype('uint8'))
    output.show()
    filename = input("Enter a filename if you would like to save this image: ")
    if filename:
        output.save(f"outputs/{filename}.jpg")


if __name__ == "__main__":
    main()
