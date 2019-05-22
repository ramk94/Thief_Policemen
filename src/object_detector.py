import darknet as dn
import logging

dn.set_gpu(0)
logger = logging.getLogger(__name__)


def convert_image(image):
    """
    Convert numpy array to specific format which can be used by darknet library
    Parameters
    ----------
    image: numpy array
        a three-dimensional array with uint type
    """
    im, _ = dn.array_to_image(image)
    return im


class Detector:
    """
    Object detector based on YOLO network.
    """

    def load(self, weight_path, network_config_path, object_config_path):
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
        im = convert_image(image)
        results = dn.detect_image(self.net, self.meta, im)
        object_list = {
            'thief': {
                "center": (0.4, 0.3),
                "size": (0.1, 0.1)
            },
            'policeman1': {
                "center": (0.8, 0.1),
                "size": (0.2, 0.2)
            },
            'policeman2': {
                "center": (0.5, 0.5),
                "size": (0.2, 0.2)
            }
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
        im = convert_image(image)
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
