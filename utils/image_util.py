from typing import Tuple
import cv2 as cv
import numpy as np

def mergeImages(image: cv.Mat, image2: cv.Mat, size2: Tuple[int, int], xy: Tuple[int, int]):
    image2 = cv.resize(image2.copy(), size2)
    image = image.copy()

    x_size = size2[0]
    y_size = size2[1]

    x_offset = xy[0]
    y_offset = xy[1]

    if image.shape[2] <= 3:
        b_channel, g_channel, r_channel = cv.split(image)
        alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255 #creating a dummy alpha channel image.
        image = cv.merge((b_channel, g_channel, r_channel, alpha_channel))
    

    alpha = image2[:,:,3]
    alpha = cv.merge([alpha,alpha,alpha,alpha])

    image[x_offset+0: x_offset+x_size , y_offset+0: y_offset+y_size ] = np.where(alpha == (0,0,0,0) , image[x_offset+0: x_offset+x_size , y_offset+0: y_offset+y_size ], image2[:,:])

    return image
