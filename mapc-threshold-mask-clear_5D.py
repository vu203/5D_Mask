#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 10:54:13 2017

@author: Vasja
"""

# 
# % reset


""" --------------- IMPORT REQUIRED PACKAGES --------------- """

import os
import matplotlib
import numpy as np
import mahotas as mh
import tifffile as tiff

import pylab
from pylab import imshow

import skimage
from skimage import morphology
from skimage import filters


""" --------------- REQUIRED USER INPUT ---------------   """


"""  1. Set folder path:  """
# This folder should contain your image file:

os.chdir('/Users/Lab/Python/image_processing') 

"""  2. Set input file name:  """
# File name in parantheses, including extension

input_file = "5D_input.tif"


"""  3. Set input file name:  """

output_file = "5D_output.tif"


"""  4. Mapping vs signal channels:  """

# Mapping channel: C1
# Signal channel: C0 

# Check this is correct, switching not currently supported. 
# See "Split channels" below to change the order of mapc and 
# signalc if necessary, and adjust accordingly in the final 
# section just before saving.


""" --------------- READ IMAGE FILES --------------- 
Tiff stacks as multi-dimensional stacks
"""

# gcio = io.imread('growthcone2C1T.tif')
# image = tf.imread('growthcone2C1T.tif')

with tiff.TiffFile(input_file) as tif:
    image = tif.asarray()
#    for page in tif:
#        for tag in page.tags.values():
#            t = tag.name, tag.value
#        image = page.asarray()

""" order: t, z, C, x, y """
""" dim: 10, 13, 2, 300, 512 """

# Split channels:

mapc    = image[:, :, 1, :, :]
signalc = image[:, :, 0, :, :]


""" --------------- THRESHOLDING --------------- 
Use simple otsu thresholding method to create binary mask
"""

# Loop Gaussian filter over timepoints:

mapc_sm = mapc.copy()
times = mapc.shape[0]
mapc_blurred = np.zeros_like(mapc_sm, dtype=float)
for i in range(times):
    print i 
    mapc_blurred[i, :, :, :] = skimage.filters.gaussian(mapc_sm[i, :, :, :], 2)

new_array2 = (mapc_blurred * 255).astype(np.uint8)
new_array2.max()

# Calculate Threshold ### USE DIFFERENT THRESHOLDING METHOD IF NECESSARY

th1 = mh.thresholding.otsu(new_array2)

# Create binary mask (as boolean matrix)

mask = (mapc > th1)


""" --------------- DILATION --------------- 
Dilate binary mask by a set number of pixels
"""

# This part is not working very well - amplifies noise, creates
# dirty patches. Use steps = 0 until finding a cleaner fixing for this 
# upstream (e.g. median filters, removing outliers, better gaussian, ...)
def multiDilate(binary_input, steps):
    curr_image = binary_input
    for i in range(steps):
        curr_image = skimage.morphology.binary_dilation(curr_image)
    return curr_image

    # To visualise how this works: 
    # imshow(multiDilate(mask, 3))

mask_dil = multiDilate(mask, 0)

# Filter the signal channel with the mask:
    

""" --------------- WRITE A FILTERED FILE ---------------
Dilate binary mask by a set number of pixels
"""

signal_filt = signalc * mask_dil

image[:, :, 0, :, :] = signal_filt
tiff.imsave(output_file, image) # does not preserve metadata!
