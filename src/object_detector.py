import darknet as dn
import logging
import cv2
import os
import numpy as np
import sys

logger = logging.getLogger(__name__)


def draw_circle(event, x, y, flags, param):
    """
    Opencv mouse click event which draws a blue circle after a double click
    """
    if event == cv2.EVENT_LBUTTONDBLCLK:
        logger.debug('mouse click at (width={0},height={1})'.format(x, y))
        image = param.get('image')
        height, width = image.shape[0], image.shape[1]
        centers = param.get('centers')
        window_name = param.get('window_name')
        cv2.circle(image, (x, y), 10, (255, 0, 0), -1)
        centers.append((x / width, y / height))
        logger.debug(
            'relative center is (width={0},height={1})'.format(x / width, y / height))
        cv2.imshow(window_name, image)


class Detector:
    """
    Object detector based on YOLO network.
    """

    def __init__(self, weight_path, network_config_path, object_config_path, auto_id=False):
        """
        Load YOLO network weights and config files

        Parameters
        ----------
        weight_path: str
            file path of YOLOv3 network weights
        network_config_path: str
            file path of YOLOv3 network configurations
        object_config_path: str
            file path of object configurations
        """
        self.net = dn.load_net(network_config_path.encode('utf-8'),
                               weight_path.encode('utf-8'), 0)
        self.meta = dn.load_meta(object_config_path.encode('utf-8'))
        self.width = dn.network_width(self.net)
        self.height = dn.network_height(self.net)
        self.policemen = {}
        self.auto_id = auto_id
        self.fake_id = 0

    def detect_objects(self, image):
        """
        Detect robots and return an object list.

        Parameters
        ----------
        image: numpy array
            an image consists of the gameing board and multiple robots

        Returns
        -------
        object_list: dict
            objects' relative locations, relative sizes and categories
            example:

        """
        im = self.convert_image(image)
        results = dn.detect_image(self.net, self.meta, im)
        results = [[result[0].decode('utf-8'), result[1], result[2]] for result in results]
        object_list = self.track_objects(results)
        logger.debug('object list: {}'.format(object_list))
        if len(object_list) < 3:
            logger.warning(
                'Only {} objects are recognized'.format(len(object_list)))
        return object_list

    def track_objects(self, detect_results):
        policemen = {}
        object_list = {}
        for result in detect_results:
            name = result[0]
            confidence = result[1]
            bounds = result[2]
            center = (bounds[0] / self.width, bounds[1] / self.height)
            size = (bounds[2] / self.width, bounds[3] / self.height)
            if name == 'policeman' and len(self.policemen) == 0:
                if self.auto_id:
                    police_id = self.fake_id
                    self.fake_id += 1
                else:
                    police_id = input("Please input a police id for object at {}".format(center))
                name = '{0}{1}'.format('policeman', police_id)
                policemen[name] = {
                    'confidence': confidence,
                    'center': center,
                    'size': size
                }
            elif name == 'policeman' and len(self.policemen) != 0:
                name = self.get_police_name_by_distance(center)
                policemen[name] = {
                    'confidence': confidence,
                    'center': center,
                    'size': size
                }
            object_list[name] = {
                'confidence': confidence,
                'center': center,
                'size': size
            }
        for key, value in policemen.items():
            self.policemen[key] = value
        for name, policeman in policemen.items():
            object_list[name] = policeman
        return object_list

    def get_police_name_by_distance(self, center):
        names = []
        distances = []
        for police_name, police in self.policemen.items():
            names.append(police_name)
            current_center = np.array(police['center']).reshape((-1, 1))
            future_center = np.array(center).reshape((-1, 1))
            distances.append(np.linalg.norm(future_center - current_center))
        index = np.argmin(distances)
        name = names[int(index)]
        return name

    def detect_gaming_board(self, image):
        """
        Analysis the gaming board image to obtain centers of triangles.

        Parameters
        ----------
        image: numpy array
            an image consists of the gaming board(may not contains robots)

        Returns
        -------
        centers: list
            relative coordinates of triangles on the gaming board(width,height)
        """
        # RBG image to BGR image for better visualization
        frame = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # build a Opencv window and set up a mouse click event
        centers = []
        window_name = 'center_tool'
        cv2.namedWindow(window_name)
        callback_params = {
            'image': frame,
            'centers': centers,
            'window_name': window_name
        }
        cv2.setMouseCallback(window_name, draw_circle, param=callback_params)
        cv2.imshow(window_name, frame)

        # wait for exit flag
        if cv2.waitKey(0) & 0xFF == ord('q'):
            cv2.destroyWindow(window_name)

        # save or read centers file
        center_file_path = 'centers.txt'
        if not centers:
            assert os.path.exists(center_file_path)
            with open(center_file_path, encoding='utf-8', mode='r') as file:
                for line in file:
                    center = tuple(map(float, line.strip().split(' ')))
                    centers.append(center)
        else:
            with open(center_file_path, encoding='utf-8', mode='w') as file:
                for center in centers:
                    file.write('{width} {height}\n'.format(
                        width=center[0], height=center[1]))
        return centers

    def convert_image(self, image):
        """
        Convert numpy array to specific format which can be used by darknet library.

        Parameters
        ----------
        image: numpy array
            a three-dimensional array with uint type

        Returns
        -------
        im: custom object
            an object which is defined by darknet library
        """
        resized_image = cv2.resize(
            image, (self.width, self.height), interpolation=cv2.INTER_LINEAR)
        im, _ = dn.array_to_image(resized_image)
        return im


if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    from camera_system import Camera

    weight_path = '../model/custom_tiny_yolov3.weights'
    network_config_path = '../cfg/custom-tiny.cfg'
    object_config_path = '../cfg/custom.data'
    detector = Detector(weight_path, network_config_path, object_config_path, auto_id=True)
    camera = Camera(1, save=False, draw=False, num_skip=0)

    window_name = 'test'
    cv2.namedWindow(window_name)

    while True:
        image = camera.get_image()
        if image is None:
            break
        image = camera.rgb_to_bgr(image)
        object_list = detector.detect_objects(image)
        boxes = camera.draw_boxes(image, object_list)
        cv2.imshow(window_name, boxes)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyWindow(window_name)
