import numpy as np


def get_image():
    """
    Capture an image from our camera.

    Returns
    ----------
    image: numpy array
        a three-dimensional numpy array which indicates an image. (I am not sure about the indexing conventions because different libraries may be different when indexing)
    """
    import cv2
    custom_image_bgr = cv2.imread('../data/processed_images/001/IMG_0897.jpg')  # use: detect(,,imagePath,)
    custom_image = cv2.cvtColor(custom_image_bgr, cv2.COLOR_BGR2RGB)
    image = cv2.resize(custom_image, (416, 416), interpolation=cv2.INTER_LINEAR)
    return image
