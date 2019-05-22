import darknet as dn
import logging
import cv2

dn.set_gpu(0)
logger = logging.getLogger(__name__)


class Detector:
    """
    Object detector based on YOLO network.
    """

    def __init__(self, weight_path, network_config_path, object_config_path):
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
        """
        im = self.convert_image(image)
        results = dn.detect_image(self.net, self.meta, im)
        object_list = {}
        police_id = 1
        for result in results:
            name = result[0].decode('utf-8')
            confidence = result[1]
            bounds = result[2]
            center = (bounds[0] / self.width, bounds[1] / self.height)
            size = (bounds[2] / self.width, bounds[3] / self.height)
            if name == 'policeman':
                name = '{0}{1}'.format('policeman', police_id)
                police_id += 1
            object_list[name] = {
                'confidence': confidence,
                'center': center,
                'size': size
            }
        return object_list

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
            relative coordinates of triangles on the gaming board
        """
        im = self.convert_image(image)
        centers = dn.detect_image(self.net, self.meta, im)
        centers = [
            (0.1, 0.6),
            (0.2, 0.2),
            (0.2, 0.4),
            (0.2, 0.8),
            (0.6, 0.2),
            (0.6, 0.5),
            (0.6, 0.6),
            (0.6, 0.7),
            (0.7, 0.9),
        ]
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
        resized_image = cv2.resize(image, (self.width, self.height), interpolation=cv2.INTER_LINEAR)
        im, _ = dn.array_to_image(resized_image)
        return im
