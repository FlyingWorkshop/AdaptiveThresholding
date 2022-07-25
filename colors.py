import numpy as np
from tqdm.notebook import tqdm
from PIL import Image
import matplotlib
import matplotlib.pyplot as plt
import cv2
import random

from collections import deque as queue


def is_valid(array, explored, point):
    if point in explored:
        return False

    x, y = point
    ymax, xmax = array.shape
    in_bounds = 0 <= x <= xmax and 0 <= y <= ymax
    if not in_bounds:
        return False

    is_white = array[x, y] == 255
    if not is_white:
        return False

    return True


def get_neighbors(center):
    x, y = center
    return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]


def bfs(array, explored, source):
    x_coords = []
    y_coords = []
    if not is_valid(array, explored, source):
        return x_coords, y_coords
    q = queue()
    q.append(source)
    while q:
        center = q.popleft()
        explored.add(center)
        x_coords.append(center[0])
        y_coords.append(center[1])
        for neighbor in get_neighbors(center):
            if is_valid(array, explored, neighbor):
                q.append(neighbor)
    return x_coords, y_coords


def main():
    img = Image.open("data/gates_of_hell_local_median_r10_gridless.jpg")

    # preprocessing
    a = np.array(img)
    a[a < 255 // 2] = 0  # black pixels
    a[a >= 255 // 2] = 255  # white pixels

    # matrix b stores RGB values, so we have to add a dimension (matrix a stores binary for black/white)
    new_shape = list(a.shape) + [3]
    b = np.repeat(a, 3).reshape(new_shape).astype(int)

    # find the contiguous white regions in the picture
    explored = set()
    for source in zip(*np.where(a == 255)):  # look for white pixels
        x_coords, y_coords = bfs(a, explored, source)
        b[x_coords, y_coords] = [181, 46, 36]
        break

    # scaling
    dpi = matplotlib.rcParams['figure.dpi']
    height, width = a.shape
    figsize = (width / float(dpi), height / float(dpi))
    plt.figure(figsize=figsize)
    # TODO: get rid of this line (debuggin)
    b[:10, :10, :10] = [181, 46, 36]
    plt.imshow(b)
    plt.show()


if __name__ == "__main__":
    main()
