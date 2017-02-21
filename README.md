# 5D_Mask

This is a simple Python script for image processing of noisy 5D image stacks. 

5D_Mask creates a binary mask from a ‘clean’ mapping channel using a global threshold of the stack (after an initial Gaussian filter). The mask is then applied to the ‘noisy’ signal channel, clearing all signal coming from outside the mask. 

The size of the mask can be expanded by the user by a set number of pixels.
