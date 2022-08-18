import numpy as np
from PIL import Image
from tqdm.notebook import tqdm

from collections import deque as queue

RNG = np.random.default_rng()


# gamma and perceptual luminance corrected grayscale weights
RED_WEIGHT = 0.299
GREEN_WEIGHT = 0.587
BLUE_WEIGHT = 0.114
RGB_WEIGHTS = [RED_WEIGHT, GREEN_WEIGHT, BLUE_WEIGHT]

# pixel values
BLACK = 0
WHITE = 255
RGB_DIMENSION = 3

def get_grayscale(image):
    """
    References:
    * What is gamma correction? (https://www.youtube.com/watch?v=wFx0d9c8WMs)
    * Convert rbg to grayscale (https://e2eml.school/convert_rgb_to_grayscale.html)
    """
    grayscale = np.dot(image[..., :3], RGB_WEIGHTS)
    return grayscale


def display(image):
    return Image.fromarray(image.astype('uint8'))


def get_custom_otsu_threshold(grayscale_image, mask):
    """
    Applies Otsu's method to a region of an image specified by a given mask
    References: https://en.wikipedia.org/wiki/Otsu%27s_method#Limitations_and_variations
    """
    intraclass_variances = []
    img = grayscale_image[mask]
    num_pixels = np.sum(mask)
    for threshold in np.arange(BLACK, WHITE):  # NOTE: black = 0, white = 255
        black_pixels = img[img < threshold]
        white_pixels = img[img >= threshold]

        if not black_pixels.any() or not white_pixels.any():
            intraclass_variance = np.inf
        else:
            black_variance = np.var(black_pixels)
            white_variance = np.var(white_pixels)
            prob_black = len(black_pixels) / num_pixels
            prob_white = len(white_pixels) / num_pixels
            intraclass_variance = prob_black * black_variance + prob_white * white_variance
        intraclass_variances.append(intraclass_variance)

    otsu_threshold = np.argmin(intraclass_variances)
    return otsu_threshold, intraclass_variances


def get_global_otsu_threshold(grayscale_image):
    mask = np.ones_like(grayscale_image, dtype=bool)
    otsu_threshold, intraclass_variances = get_custom_otsu_threshold(grayscale_image, mask)
    return otsu_threshold, intraclass_variances


def adaptive_median_thresholding(grayscale_image, radius):
    bw_image = np.zeros_like(grayscale_image)
    max_row, max_col = grayscale_image.shape
    for i, row in enumerate(tqdm(grayscale_image)):
        y_min = max(0, i - radius)
        y_max = min(max_row, i + radius + 1)
        for j, elem in enumerate(row):
            x_min = max(0, j - radius)
            x_max = min(max_col, j + radius + 1)
            window = grayscale_image[y_min:y_max, x_min:x_max]
            if grayscale_image[i, j] >= np.median(window):
                bw_image[i, j] = WHITE
    return bw_image

def _is_square(a: np.ndarray):
    if len(a.shape) != 2:
        return False
    if a.shape[0] != a.shape[1]:
        return False
    return True


def _is_valid(array, seen, point):
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


def _get_neighbors(center):
    x, y = center
    return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]


def _bfs(array, seen, source):
    y_coords = []
    x_coords = []
    if not _is_valid(array, seen, source):
        return y_coords, x_coords
    q = queue()
    q.append(source)
    seen.add(source)
    while q:
        center = q.popleft()
        y_coords.append(center[0])  # remember numpy indexing is flipped!
        x_coords.append(center[1])
        neighbors = _get_neighbors(center)
        for neighbor in neighbors:
            if _is_valid(array, seen, neighbor):
                seen.add(neighbor)
                q.append(neighbor)
    return y_coords, x_coords


def fillcolor(bw_image, mask: np.ndarray | None):
    # matrix b stores RGB values, so we have to add a dimension (matrix a stores binary for black/white)
    new_shape = list(bw_image.shape) + [RGB_DIMENSION]
    colored = np.repeat(bw_image, RGB_DIMENSION).reshape(new_shape).astype(int)

    # find the contiguous white regions in the picture
    if mask is None:
        explored = set()
    else:
        explored = set(zip(*np.where(mask)))
    for source in tqdm(list(zip(*np.where(bw_image == WHITE)))):  # look for white pixels
        x_coords, y_coords = _bfs(bw_image, explored, source)
        colored[x_coords, y_coords] = RNG.integers(low=BLACK, high=WHITE, size=RGB_DIMENSION)

    return colored
