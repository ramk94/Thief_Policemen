import numpy as np
import cv2

def get_image():
    """
    Capture an image from our camera.

    Returns
    ----------
    image: numpy array
        a three-dimensional numpy array which indicates an image, and the shape of this array is (height,width,channels). For example, if an image has height 512, width 384, then the array's shape should be (512,384,3). Note that the color order should be RGB, and the left-top corner of the image represents coordinate (0,0).
    """
    custom_image_bgr = cv2.imread('../data/processed_images/001/IMG_0897.jpg')
    image = cv2.cvtColor(custom_image_bgr, cv2.COLOR_BGR2RGB) # BGR to RGB
    return image
