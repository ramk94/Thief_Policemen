import numpy as np
import cv2
import uuid

cap = cv2.VideoCapture(1)


def get_image(save=True):
    """
    Capture an image from our camera.

    Returns
    ----------
    image: numpy array
        a three-dimensional numpy array which indicates an image, and the shape of this array is (height,width,channels). For example, if an image has height 512, width 384, then the array's shape should be (512,384,3). Note that the color order should be RGB, and the left-top corner of the image represents coordinate (0,0).
    """
    flag, frame = cap.read()
    if flag:
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    else:
        custom_image_bgr = cv2.imread(
            '../data/processed_images/001/IMG_0897.jpg')
        image = cv2.cvtColor(custom_image_bgr, cv2.COLOR_BGR2RGB)  # BGR to RGB
    if save:
        cv2.imwrite('../data/pics/{}.png'.format(uuid.uuid1()),
                    cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    return image
