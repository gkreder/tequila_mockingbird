from skimage.morphology import watershed, disk
from skimage.filters import sobel
from skimage import exposure
from skimage import transform as tf
from skimage.segmentation import slic, join_segmentations
from skimage import data, img_as_float
from scipy import fftpack
from skimage.filters.rank import median
from scipy import ndimage as ndi
from skimage import data
# ----------------------------------------------------------------------
import skimage.feature
import skimage.filters
import os
import sys
import skimage
import nd2reader
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy.misc
import numpy as np
GIT_DIR = os.path.normpath(os.path.dirname(os.getcwd()))
PUBS_DIR = os.path.normpath(os.path.dirname(GIT_DIR))
IMAGE_DIR = os.path.normpath(PUBS_DIR + '/images_day_1/')
# ----------------------------------------------------------------------
def segment_BF(img):

	global_thresh = skimage.filters.threshold_otsu(img)
	binary_global = img > global_thresh
	elevation_map = binary_global

	markers = np.zeros_like(img)
	markers[img > np.mean(img) - 200] = 1
	markers[img < np.mean(img) - 200] = 2
	# markers = skimage.morphology.closing(markers)
	# markers = ndi.binary_fill_holes(markers - 1)

	segmentation = watershed(elevation_map, markers)

	segmentation = skimage.morphology.closing(segmentation)	

	segmentation = ndi.binary_fill_holes(segmentation - 1)
	segmentation_first_filter = skimage.morphology.remove_small_objects(segmentation, 200)
	segmentation_second_filter = skimage.morphology.remove_small_objects(segmentation, 800)
	segmentation_second_filter = np.invert(segmentation_second_filter)
	segmentation_final = np.multiply(segmentation_first_filter, segmentation_second_filter)
	labeled_img, num_objects = ndi.label(segmentation_final)
	image_label_overlay = skimage.color.label2rgb(labeled_img, image=img)

	plt.imshow(img, cmap=plt.cm.gray, interpolation='nearest')
	plt.contour(segmentation_final, [0.5], linewidths=1.2, colors='y')
	# plt.imshow(image_label_overlay)
	# plt.imshow(markers, cmap = plt.cm.gray)
	plt.show()

	return labeled_img, num_objects


def segment_DAPI(img):
	marker_mat = np.zeros_like(img)
	global_thresh = skimage.filters.threshold_otsu(img)
	binary_global = img > global_thresh
	sobel_edges = sobel(img)

	markers = binary_global + 1
	segmentation = watershed(sobel_edges, markers)
	segmentation = ndi.binary_fill_holes(segmentation - 1)

	labeled_img, num_objects = ndi.label(segmentation)
	image_label_overlay = skimage.color.label2rgb(labeled_img, image=img)

	# print object_labels
	# plt.imshow(labeled_coins) 
	# plt.show()s

	return labeled_img, num_objects

def get_object_indices(labeled_img):
	object_labels = []
	for row in labeled_img:
		for element in row:
			if element not in object_labels and element != 0:
				object_labels.append(element)
	return object_labels

# ------------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------------
# IMAGE_NAME = '/Plate000_WellA12_Seq0011C1XY1.tif'
# im_path = IMAGE_DIR + IMAGE_NAME
# im = scipy.misc.imread(im_path)
# # print im
# labeled_img, num_objects = segment_DAPI(im)
# # plt.imshow(labeled_img)
# # plt.show()


IMAGE_NAME = '/Plate000_WellA12_Seq0011C5XY1.tif'
im_path = IMAGE_DIR + IMAGE_NAME
im = scipy.misc.imread(im_path)
# print im
segment_BF(im)
# plt.imshow(im)
# plt.show()

