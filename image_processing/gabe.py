from skimage.morphology import watershed, disk
from skimage.filters import sobel
from skimage import exposure
from skimage import transform as tf
from skimage.segmentation import slic, join_segmentations
from skimage import data, img_as_float
from scipy import fftpack
from skimage.filters.rank import median
from scipy import ndimage as ndi

# ----------------------------------------------------------------------
import os
import sys
import skimage
import nd2reader
import matplotlib as mpl
import matplotlib.pyplot as plt
GIT_DIR = os.path.normpath(os.path.dirname(os.getcwd()))
PUBS_DIR = os.path.normpath(os.path.dirname(GIT_DIR))
IMAGE_DIR = os.path.normpath(PUBS_DIR + '/images_day_1/')
# ----------------------------------------------------------------------

def segment_image(photo_matrix, background_threshold, foreground_threshold):
    edges = sobel(photo_matrix)
    markers = np.zeros_like(photo_matrix)
    foreground, background = 1, 2
    markers[photo_matrix < background_threshold] = background
    markers[photo_matrix > foreground_threshold] = foreground
    ws = watershed(edges, markers)
    segmentation_matrix = ndi.label(ws == foreground)[0]
    return segmentation_matrix



# IMAGE_NAME = '/Plate000_WellA12_Seq0011.nd2'
# im_path = IMAGE_DIR + IMAGE_NAME
# nd2 = nd2reader.Nd2(im_path)
# for image in nd2.select(channels = 'DAPI'):
# 	plt.imshow(image)
# 	plt.show()




