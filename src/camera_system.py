import numpy as np


def get_image():
    """
    Capture an image from our camera.

    Returns
    ----------
    image: numpy array
        a three-dimensional numpy array which indicates an image. (I am not sure about the indexing conventions because different libraries may be different when indexing)
    """
    image = np.random((1920, 1080, 3))
    return image
