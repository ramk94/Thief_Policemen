import cv2
import uuid
import os

cap = cv2.VideoCapture(0)
COLORS = {
    'thief': (255, 0, 0),
    'policeman1': (0, 255, 0),
    'policeman2': (0, 0, 255)
}
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 1
LINE_TYPE = 2


class Camera:
    def __init__(self, camera_id=0, draw=True, save=True, save_path='../data/pics', num_skip=10, window_name='main'):
        self.draw = draw
        self.save = save
        self.save_path = save_path
        self.cap = cv2.VideoCapture(camera_id)
        self.num_skip = num_skip
        self.window_name = window_name
        if self.draw:
            cv2.namedWindow(window_name)

    def __del__(self):
        self.cap.release()
        if self.draw:
            cv2.destroyWindow(self.window_name)

    def _skip_frames(self):
        for i in range(self.num_skip):
            self.cap.read()

    def get_image(self):
        self._skip_frames()
        flag, frame = self.cap.read()
        if flag:
            if self.save:
                cv2.imwrite(os.path.join(self.save_path, '{}.jpg'.format(uuid.uuid1())), frame)
            if self.draw:
                self.display(frame)
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        else:
            image = None
        return image

    @staticmethod
    def draw_boxes(image, object_list):
        if len(object_list) > 0:
            for key, value in object_list.items():
                height, width = image.shape[0], image.shape[1]
                x = int(value['center'][0] * width)
                y = int(value['center'][1] * height)
                size_width = value['size'][0] * width
                size_height = value['size'][1] * height
                x1 = int(x - size_width / 2)
                y1 = int(y - size_height / 2)
                x2 = int(x + size_width / 2)
                y2 = int(y + size_height / 2)
                color = COLORS.get(key, (255, 255, 255))
                cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
                cv2.putText(image, key,
                            (x1 - 10, y1 - 10),
                            FONT,
                            FONT_SCALE,
                            color,
                            LINE_TYPE)
        return image

    def display(self, image):
        cv2.imshow(self.window_name, image)
        cv2.waitKey(1)

    @staticmethod
    def bgr_to_rgb(frame):
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return image

    @staticmethod
    def rgb_to_bgr(frame):
        image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        return image


def get_image(save=True, save_path='../data/pics'):
    """
    Capture an image from our camera.

    Returns
    ----------
    image: numpy array
        a three-dimensional numpy array which indicates an image, and the shape of this array is (height,width,channels). For example, if an image has height 512, width 384, then the array's shape should be (512,384,3). Note that the color order should be RGB, and the left-top corner of the image represents coordinate (0,0).
    """

    # drop previous images to avoid duplication
    for i in range(10):
        cap.read()
    #
    flag, frame = cap.read()
    if flag:
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    else:
        image = None
    if image is not None and save:
        cv2.imwrite(os.path.join(save_path, '{}.jpg'.format(uuid.uuid1())), cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    return image
