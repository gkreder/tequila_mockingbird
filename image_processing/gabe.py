from skimage.morphology import watershed, disk
from skimage.filters import sobel
from skimage import exposure
from skimage import transform as tf
from skimage.segmentation import slic, join_segmentations
from skimage import data, img_as_float
from scipy import fftpack
from skimage.filters.rank import median
from scipy import ndimage as ndi

def segment_image(photo_matrix, background_threshold, foreground_threshold):
    edges = sobel(photo_matrix)
    markers = np.zeros_like(photo_matrix)
    foreground, background = 1, 2
    markers[photo_matrix < background_threshold] = background
    markers[photo_matrix > foreground_threshold] = foreground
    ws = watershed(edges, markers)
    segmentation_matrix = ndi.label(ws == foreground)[0]
    return segmentation_matrix






