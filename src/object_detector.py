import darknet as dn
import logging
import cv2

logger = logging.getLogger(__name__)


def draw_circle(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        logger.debug('mouse click at (width={0},height={1})'.format(x, y))
        image = param.get('image')
        height, width = image.shape[0], image.shape[1]
        centers = param.get('centers')
        window_name = param.get('window_name')
        cv2.circle(image, (x, y), 10, (255, 0, 0), -1)
        centers.append((x/width, y/height))
        logger.debug(
            'relative center is (width={0},height={1})'.format(x/width, y/height))
        cv2.imshow(window_name, image)


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
            example:
            {
                "thief":{
                    "confidence":0.99,
                    "center":(0.16,0.37), # (width,height)
                    "size":(0.21,0.25), # (width,height)
                }
            }
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
            relative coordinates of triangles on the gaming board(width,height)
        """
        centers = []
        window_name = 'center_tool'
        cv2.namedWindow(window_name)
        cv2.setMouseCallback(window_name, draw_circle, param={
                             'image': image, 'centers': centers, 'window_name': window_name})
        cv2.imshow(window_name, image)
        if cv2.waitKey(0) & 0xFF == ord('q'):
            cv2.destroyWindow(window_name)
        if not centers:
            with open('centers.txt', encoding='utf-8', mode='r') as file:
                for line in file:
                    center = tuple(map(float, line.strip().split(' ')))
                    centers.append(center)
        else:
            with open('centers.txt', encoding='utf-8', mode='w') as file:
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
