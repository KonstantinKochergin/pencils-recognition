import matplotlib.pyplot as plt
import numpy as np
from skimage.color import rgb2gray
from skimage.filters import threshold_otsu
from skimage.measure import label, regionprops
from skimage.morphology import skeletonize

def proportion(width, height):
    return max(width, height) / min(width, height)

def filling_factor(region):
    return region.area / (region.image.shape[0] * region.image.shape[1])

area_min = 20000

pencils_count = 0
for i in range(1, 13): #1, 13
    image = plt.imread(f"images/img ({i}).jpg")
    gray = rgb2gray(image)
    threshold = threshold_otsu(gray)
    binary = (gray < threshold).astype(int)
    labeled = label(binary)
    regions = regionprops(labeled)
    rest_regions = []
    for region in regions:
        if region.area < area_min:
            labeled[np.where(labeled == region.label)] = 0
        else:
            rest_regions.append(region)
    count_on_image = 0
    for reg in rest_regions:
        width = reg.image.shape[1]
        height = reg.image.shape[0]
        pr = proportion(width, height)
        if pr > 10 and min(width, height) > 100:
            count_on_image += 1
            pencils_count += 1
        elif filling_factor(reg) < 0.23 and max(width, height) > 1800:
            count_on_image += 1
            pencils_count += 1
    print(f"pencils on image {i} = {count_on_image}")

print(f"pencils count = {pencils_count}")
