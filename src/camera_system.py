import numpy as np
import cv2

def get_image():
    """
    Capture an image from our camera.

    Returns
    ----------
    image: numpy array
        a three-dimensional numpy array which indicates an image. (I am not sure about the indexing conventions because different libraries may be different when indexing)
    """
    custom_image_bgr = cv2.imread('../data/processed_images/001/IMG_0897.jpg')  # use: detect(,,imagePath,)
    image = cv2.cvtColor(custom_image_bgr, cv2.COLOR_BGR2RGB)
    return image
