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

	sobel_edges = sobel(img)
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
	# plt.imshow(sobel_edges, cmap = plt.cm.gray)
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


	# plt.imshow(segmentation, cmap = plt.cm.gray) 
	plt.imshow(img, cmap = plt.cm.gray)
	plt.contour(segmentation, [0.5], linewidths=1.2, colors='y')
	plt.show()

	return labeled_img, num_objects

def find_nuclei(img, dapi_cells):



	# ------------------------------------------------------------
	# Total Image Maxima
	# ------------------------------------------------------------
	# img = skimage.img_as_float(img)
	# local_peaks = skimage.feature.peak_local_max(img, min_distance = 20, threshold_abs = 0.1)
	# # print local_peaks
	# blank_image = np.zeros_like(img)
	# for row, column in local_peaks:
	# 	blank_image[row, column] = 1

	# plt.imshow(img, cmap=plt.cm.gray, interpolation='nearest')
	# plt.contour(blank_image, [0.5], linewidths=1.2, colors='y')
	# plt.contour(dapi_cells, [0.5], linewidths=1.2, colors='y')
	# ------------------------------------------------------------



	# ----------------------------------------------------------------
	# Single cell masking
	# ----------------------------------------------------------------
	object_labels = get_object_labels(dapi_cells)	
	nuclei_labeled = []
	nuclei = []
	for label in object_labels:
	# label = 500
		masked_image = np.zeros_like(dapi_cells)
		img_copy = np.copy(img)
		img_copy[dapi_cells != label] = 0
		local_peaks = skimage.feature.peak_local_max(img_copy, num_peaks = 1)
		if len(local_peaks) > 0:
			peak_row, peak_column = local_peaks[0]
			nuclei_labeled.append(([peak_row, peak_column], label))
			# img[peak_row, peak_column] = 0.0

	# plt.imshow(img, cmap=plt.cm.gray, interpolation='nearest')
	# plt.show()
	# ----------------------------------------------------------------

	# masked_image[dapi_cells == label] = 1

		

	# print dapi_cells




	# image_label_overlay = skimage.color.label2rgb(dapi_cells, image=img)
	# plt.imshow(image_label_overlay, cmap = plt.cm.gray)

	# plt.imshow(img, cmap=plt.cm.gray, interpolation='nearest')
	# plt.contour(segmentation_final, [0.5], linewidths=1.2, colors='y')


	# plt.imshow(img_copy, cmap = plt.cm.gray)
	return nuclei_labeled



def get_object_labels(labeled_img):
	object_labels = np.unique(labeled_img)
	object_labels = object_labels[1 : ]
	return object_labels

# ------------------------------------------------------------------------
# MAIN
# ------------------------------------------------------------------------

# ------------------------------------------------
# DAPI Segmentation
# ------------------------------------------------
IMAGE_NAME = '/Plate000_WellA12_Seq0011C1XY1.tif'
im_path = IMAGE_DIR + IMAGE_NAME
im = scipy.misc.imread(im_path)
# print im
labeled_img, num_objects = segment_DAPI(im)
# plt.imshow(labeled_img)
# plt.show()
# ------------------------------------------------
# ------------------------------------------------


# ------------------------------------------------
# BF
# ------------------------------------------------
# IMAGE_NAME = '/Plate000_WellA12_Seq0011C5XY1.tif'
# im_path = IMAGE_DIR + IMAGE_NAME
# im = scipy.misc.imread(im_path)
# # print im
# segment_BF(im)
# # plt.imshow(im)
# # plt.show()
# ------------------------------------------------
# ------------------------------------------------

# ------------------------------------------------
# Find nuclei
# ------------------------------------------------
# IMAGE_NAME = '/Plate000_WellA12_Seq0011C1XY1.tif'
# im_path = IMAGE_DIR + IMAGE_NAME
# im = scipy.misc.imread(im_path)
# labeled_img, num_objects = segment_DAPI(im)
# # print im
# find_nuclei(im, labeled_img)
# # # plt.imshow(labeled_img)
# # # plt.show()
# ------------------------------------------------
# ------------------------------------------------



