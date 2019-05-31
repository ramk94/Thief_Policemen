import numpy as np
import logging
from robot_client import Robot
logger = logging.getLogger(__name__)


class Controller:
    """
    Control system is the most important part of our project.
    """

    def __init__(self):
        self.robot_client = Robot('thief', '192.168.1.106', 4242)
        self.last_vector = None

    def calculate_control_signals(self, centers, object_list, instructions, sensor_data=None):
        """
        calculate real control signals based on instructions. Now the calculation is based on a simple strategy: rotate gamma degree and move forward one unit.

        Parameters
        ----------
        centers: list
            centers' coordinates of triangles on the gaming board
        object_list: dict
            objects' relative locations, relative sizes and categories
        instructions: dict
            a dict consists of future decisions

        Returns
        -------
        signals: dict
            control signals based on instructions
        """
        if sensor_data is None:
            sensor_data = self.get_sensor_data()
        signals = []
        for key, value in object_list.items():
            # get orientation information
            orientation = sensor_data[key]['orientation']

            # build orientation unit vectors
            current_direction = np.array(
                orientation['current'][0:2]).reshape((-1, 1))
            current_direction = current_direction / \
                np.linalg.norm(current_direction)
            base_unit_vector = np.array(
                orientation['base'][0:2]).reshape((-1, 1))
            base_unit_vector = base_unit_vector / \
                np.linalg.norm(base_unit_vector)

            # build center vectors
            current_center = np.array(value['center']).reshape((-1, 1))
            next_center = np.array(
                centers[instructions[key][1]-1]).reshape((-1, 1))

            # calculate the angle between centers
            delta = next_center - current_center
            dot = np.dot(base_unit_vector.T, delta)
            det = base_unit_vector[0] * delta[1] - \
                base_unit_vector[1] * delta[0]
            theta = np.arctan2(det, dot)

            # calculate the angle between orientations
            dot = np.dot(base_unit_vector.T, current_direction)
            det = base_unit_vector[0] * current_direction[1] - \
                base_unit_vector[1] * current_direction[0]
            alpha = np.arctan2(det, dot)

            # calculate rotate angle
            gamma = (theta - alpha) * 180 / np.pi

            # construct rotate signal
            signals.append({
                'name': key,
                'type': 'rotate',
                'param': gamma.item()
            })

            # construct move signal
            signals.append({
                'name': key,
                'type': 'move',
                'param': 1
            })
        return signals

    def get_orientation(self):
        self.robot_client.move_forward(4)
        self.robot_client.rotate(180)
        self.robot_client.move_forward(4)
        self.robot_client.rotate(180)

    def get_sensor_data(self):
        """
        Collect senor data from robots.

        Returns
        -------
        sensor_data: dict
            sensor data like orientations(x,y,z)
            example:
                sensor_data = {
                    'thief': {
                        'orientation': {
                            'base': (0, 1, 3),
                            'current': (1, 0, 1.5)
                        }
                    },
                    'policeman1': {
                        'orientation': {
                            'base': (0, 1, 3),
                            'current': (1, 0, 1.5)
                        }
                    },
                    'policeman2': {
                        'orientation': {
                            'base': (0, 1, 3),
                            'current': (1, 0, 1.5)
                        }
                    }
                }
        """
        sensor_data = {
            'thief': {
                'orientation': {
                    'base': (0, 1, 3),
                    'current': (1, 0, 1.5)
                }
            },
            'policeman1': {
                'orientation': {
                    'base': (0, 1, 3),
                    'current': (1, 0, 1.5)
                }
            },
            'policeman2': {
                'orientation': {
                    'base': (0, 1, 3),
                    'current': (1, 0, 1.5)
                }
            }
        }
        return sensor_data

    def move_robots(self, control_signals):
        """
        Move robots with control signals.

        Parameters
        -------
        control_signals: dict
            control signals based on instructions
        """

    def is_finished(self, centers, object_list, instructions, threshold=0.05):
        """
        Check if the movement is done.

        Parameters
        ----------
        centers: list
            centers' coordinates of triangles on the gaming board
        object_list: dict
            objects' relative locations, relative sizes and categories
        instructions:dict
            a dict consists of future decisions

        Returns
        -------
        is_done: bool
            True if all robots are at correct locations, otherwise False
        """
        is_done = True
        for key, value in object_list.items():
            current_center = np.array(value['center'])
            target = instructions[key][1]
            target_center = np.array(centers[target-1])
            print("error: "+str(np.linalg.norm(current_center-target_center)))
            if np.linalg.norm(current_center-target_center) <= threshold:
                logger.info('{0} has moved to node {1}.'.format(key, target))
            else:
                is_done = False
                logger.info(
                    '{0} has not moved to node {1}.'.format(key, target))
        return is_done


if __name__ == '__main__':
    import cv2
    from camera_system import get_image
    from object_detector import Detector

    WEIGHT_PATH = '../model/custom_tiny_yolov3.weights'
    NETWORK_CONFIG_PATH = '../cfg/custom-tiny.cfg'
    OBJECT_CONFIG_PATH = '../cfg/custom.data'
    detector = Detector(WEIGHT_PATH, NETWORK_CONFIG_PATH, OBJECT_CONFIG_PATH)

    window_name = 'test'
    cv2.namedWindow(window_name)
    # wait for exit flag
    object_list = []
    while len(object_list) == 0:
        image = get_image(save=True)
        object_list = detector.detect_objects(image)
    print(object_list)

    p1 = np.array(object_list['thief']['center']).reshape((-1, 1))

    if len(object_list) > 0:
        for key, value in object_list.items():
            height, width = image.shape[0], image.shape[1]
            cv2.circle(
                image, (int(value['center'][0]*width), int(value['center'][1]*height)), 10, (255, 0, 0), -1)
    cv2.imshow(window_name, image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
    centers = [
        (0.62, 0.72),
        (0.59, 0.46)
    ]
    controller = Controller()
    controller.robot_client.move_forward(4)
    # controller.robot_client.rotate(180)

    object_list = []
    while len(object_list) == 0:
        image = get_image(save=True)
        object_list = detector.detect_objects(image)
    p2 = np.array(object_list['thief']['center']).reshape((-1, 1))

    sensor_data = {
        'thief': {
            'orientation': {
                'base': (0, 1, 3),
                'current': ((p2-p1)[0], (p2-p1)[1], 1.5)
            }
        }
    }
    target_vector = np.array(centers[1]).reshape((-1, 1))
    controller.last_vector = target_vector-p2

    signals = controller.calculate_control_signals(
        centers, object_list, {'thief': (1, 2)}, sensor_data)
    alpha = int(signals[0]['param'])+20
    print('alpha is {}'.format(alpha))
    controller.robot_client.rotate(alpha)

    vector_previous = np.array(object_list['thief']['center']).reshape((-1, 1))

    while not controller.is_finished(centers, object_list, {'thief': (1, 2)}):
        target_vector = np.array(centers[1]).reshape((-1, 1))
        controller.robot_client.move_forward(2)
        object_list = []
        while len(object_list) == 0:
            image = get_image(save=True)
            object_list = detector.detect_objects(image)
        print(object_list)
        vector_current = np.array(
            object_list['thief']['center']).reshape((-1, 1))
        sensor_data = {
            'thief': {
                'orientation': {
                    'base': (0, 1, 3),
                    'current': ((vector_current-vector_previous)[0], (vector_current-vector_previous)[1], 1.5)
                }
            }
        }

        def unit_vector(vector):
            return vector/np.linalg.norm(vector)

        def angle_between(v1, v2):
            v1_u = unit_vector(v1)
            v2_u = unit_vector(v2)
            return np.arccos(np.dot(v1_u.T, v2_u))/np.pi*180
        rotate = False
        current_direction = vector_current-vector_previous
        controller.last_vector = target_vector-vector_current
        alpha = angle_between(current_direction, controller.last_vector).item()
        alpha = int(alpha)
        if alpha > 30:
            rotate = True
        print('alpha is {}'.format(alpha))
        rotate = False
        if rotate:
            controller.robot_client.rotate(alpha)
        if len(object_list) > 0:
            for key, value in object_list.items():
                height, width = image.shape[0], image.shape[1]
                cv2.circle(
                    image, (int(value['center'][0]*width), int(value['center'][1]*height)), 10, (255, 0, 0), -1)
        cv2.imshow(window_name, image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        vector_previous = vector_current
    print('done')
    cv2.destroyAllWindows()
