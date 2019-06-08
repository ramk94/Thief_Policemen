import numpy as np
import logging
from robot_client import Robot
import json

logger = logging.getLogger(__name__)


def get_unit_vector(vec):
    return vec / np.linalg.norm(vec)


def calculate_angle(current_center, target_center, base_direction, current_direction):
    # build orientation unit vectors
    current_direction_unit = get_unit_vector(current_direction)
    base_direction_unit = get_unit_vector(base_direction)

    # calculate the angle between centers
    delta = target_center - current_center
    delta_unit = get_unit_vector(delta)
    dot = np.dot(base_direction_unit.T, delta_unit)
    det = np.cross(delta_unit.flatten(), base_direction_unit.flatten())
    theta = np.arctan2(det, dot) * 180 / np.pi

    # calculate the angle between orientations
    dot = np.dot(base_direction_unit.T, current_direction_unit)
    det = np.cross(current_direction_unit.flatten(),
                   base_direction_unit.flatten())
    alpha = np.arctan2(det, dot) * 180 / np.pi

    # calculate rotate angle
    gamma = alpha - theta

    return gamma.item()


class Controller:
    """
    Control system is the most important part of our project.
    """

    def __init__(self, detector, get_image, robots_config_path=None):
        """
        Construct controller by a robot config file.

        Parameters
        -------
        robots_config_path: str
            file path of robots config file
        """
        self.object_list = {}
        self.detector = detector
        self.get_image = get_image
        self.sensors = {}
        self.robots = {}
        if robots_config_path:
            with open(robots_config_path, mode='r', encoding='utf-8') as file:
                robots_config = json.load(file)
                for key, value in robots_config.items():
                    robot = Robot(key, value['ip'], value['port'])
                    self.robots[key] = robot
        else:
            # testing code
            self.robot_client = Robot('thief', '192.168.1.106', 4242)
            self.last_vector = None

    def connect(self):
        """
        Connect to robots.
        """
        for key, robot in self.robots.items():
            robot.connect()

    def calculate_control_signals(self, centers, object_list, instructions, sensor_data=None, threshold=0.05):
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
        sensor_data: dict
            a dict consists of orientation data(only use sensor when sensor_data is None)
        threshold: float
            a float value indicates the threshold of distance between centers

        Returns
        -------
        signals: dict
            control signals based on instructions
        """
        if sensor_data is None:
            sensor_data = {}
        signals = []
        for key, value in object_list.items():

            # if no available sensor data, call robot function
            if key not in sensor_data:
                result = self.get_sensor_data(key)
                if result is not None:
                    sensor_data[key] = result
                else:
                    raise Exception('cannot obtain sensor data')

            # get orientation information
            orientation = sensor_data[key]['orientation']

            # build orientation unit vectors
            current_direction = np.array(orientation['current']).reshape((-1, 1))
            base_direction = np.array(orientation['base']).reshape((-1, 1))

            # build center vectors
            current_center = np.array(value['center']).reshape((-1, 1))
            target_center = np.array(centers[instructions[key][1] - 1]).reshape((-1, 1))

            # calculate angle
            gamma = calculate_angle(current_center, target_center, base_direction, current_direction)

            # calculate euclidean distance between current position and target center
            distance = np.linalg.norm(current_center - target_center)

            # only return control signals when the distance is larger than the threshold
            if distance > threshold:
                # construct rotate signal
                signals.append({
                    'name': key,
                    'type': 'rotate',
                    'param': int(gamma)
                })

                # construct move signal
                signals.append({
                    'name': key,
                    'type': 'move',
                    'param': 1
                })
        return signals

    def get_sensor_data(self, name):
        """
        Collect senor data from a robot with its name.

        Parameters
        ----------
        name: str
            robot's name

        Returns
        -------
        sensor_data: dict
            sensor data like orientations(x,y)
            example:
                sensor_data = {
                        'orientation': {
                            'base': (0, -1),
                            'current': (1, 0)
                        }
        """
        robot = self.robots[name]
        sensor_data = robot.get_sensor_data()
        if 'data' not in sensor_data or sensor_data['data'] is None:
            if name not in self.sensors:
                sensor_data = self.get_orientation_by_camera(name)
            else:
                sensor_data = self.sensors[name]
        self.sensors[name] = sensor_data
        return sensor_data

    def get_orientation_by_camera(self, name):
        # get robot instance by name
        robot = self.robots[name]

        # get previous location
        object_list = {}
        while name not in object_list:
            image = self.get_image()
            object_list = self.detector.detect_objects(image)
        previous_center = object_list[name]['center']
        previous_center_vector = np.array(previous_center).reshape((-1, 1))

        # slightly move the robot
        robot.move_forward(2)

        # get current location
        object_list = {}
        while name not in object_list:
            image = self.get_image()
            object_list = self.detector.detect_objects(image)
        current_center = object_list[name]['center']
        current_center_vector = np.array(current_center).reshape((-1, 1))

        # calculate direction
        direction = current_center_vector - previous_center_vector

        # construct result
        result = {
            'orientation': {
                'base': (0, -1),
                'current': (direction[0], direction[1])
            }
        }
        return result

    def update_state(self, object_list):
        if self.object_list == {}:
            self.object_list = object_list
        else:
            previous_object_list = self.object_list
            self.object_list = object_list
            post_object_list = object_list
            for name in object_list.keys():
                self.sensors[name]['orientation']['current'] = (
                    post_object_list[name]['center'][0] - previous_object_list[name]['center'][0],
                    post_object_list[name]['center'][1] - previous_object_list[name]['center'][1])

    def move_robots(self, control_signals):
        """
        Move robots with control signals.

        Parameters
        -------
        control_signals: dict
            control signals based on instructions
        """
        results = []
        for signal in control_signals:
            robot_name = signal['name']
            command_type = signal['type']
            param = signal['param']
            robot = self.robots[robot_name]
            if command_type == 'rotate':
                result = robot.rotate(param)
            elif command_type == 'move':
                result = robot.move_forward(param)
            else:
                message = 'invalid robot command type: {}'.format(command_type)
                raise Exception(message)
            results.append(result)
        return results

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
            # get current center coordinates
            current_center = np.array(value['center'])

            # get target center coordinates
            target = instructions[key][1]
            target_center = np.array(centers[target - 1])

            # calculate euclidean distance between current center and target center
            distance = np.linalg.norm(current_center - target_center)
            message = "{0}: {1} -> {2} = {3}".format(
                key, current_center, target_center, distance)
            logger.info(message)

            # if distance is too big, then is_done is False
            if distance <= threshold:
                message = '{0} has moved to node {1}.'.format(key, target)
                logger.info(message)
            else:
                is_done = False
                message = '{0} has not moved to node {1}.'.format(key, target)
                logger.info(message)
        return is_done


if __name__ == '__main__':
    import cv2
    from camera_system import get_image
    from object_detector import Detector

    WEIGHT_PATH = '../model/custom_tiny_yolov3.weights'
    NETWORK_CONFIG_PATH = '../cfg/custom-tiny.cfg'
    OBJECT_CONFIG_PATH = '../cfg/custom.data'
    ROBOTS_CONFIG_PATH = '../cfg/robots.json'
    detector = Detector(WEIGHT_PATH, NETWORK_CONFIG_PATH, OBJECT_CONFIG_PATH)
    centers = [
        (0.62, 0.72),
        (0.43, 0.30)
    ]
    window_name = 'test'
    cv2.namedWindow(window_name)


    def get_object_list():
        obj_list = {}
        img = None
        while len(obj_list) == 0:
            img = get_image()
            obj_list = detector.detect_objects(img)
            for kk, oo in object_list.items():
                hh, ww = img.shape[0], img.shape[1]
                cv2.circle(
                    image, (int(oo['center'][0] * ww), int(oo['center'][1] * hh)), 10, (255, 0, 0), -1)
        return obj_list, img


    object_list, image = get_object_list()
    print(object_list)

    p1 = np.array(object_list['thief']['center']).reshape((-1, 1))

    height, width = image.shape[0], image.shape[1]
    x = int(centers[1][0] * width)
    y = int(centers[1][1] * height)
    cv2.circle(image, (x, y), 20, (0, 255, 0), -1)
    cv2.imshow(window_name, image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()

    controller = Controller(detector, ROBOTS_CONFIG_PATH)
    controller.robot_client.move_forward(4)

    object_list, image = get_object_list()

    p2 = np.array(object_list['thief']['center']).reshape((-1, 1))

    current_direction = p2 - p1

    sensors = {
        'thief': {
            'orientation': {
                'base': (0, -1),
                'current': (current_direction[0], current_direction[1])
            }
        }
    }

    target_vector = np.array(centers[1]).reshape((-1, 1))
    controller.last_vector = target_vector - p2

    signals = controller.calculate_control_signals(
        centers, object_list, {'thief': (1, 2)}, sensors)
    alpha = int(signals[0]['param'])
    print('alpha is {}'.format(alpha))
    controller.robot_client.rotate(alpha)

    vector_previous = np.array(object_list['thief']['center']).reshape((-1, 1))

    while not controller.is_finished(centers, object_list, {'thief': (1, 2)}):
        target_vector = np.array(centers[1]).reshape((-1, 1))

        controller.robot_client.move_forward(2)

        object_list = []
        while len(object_list) == 0:
            image = get_image()
            object_list = detector.detect_objects(image)
        print(object_list)
        vector_current = np.array(
            object_list['thief']['center']).reshape((-1, 1))
        sensors = {
            'thief': {
                'orientation': {
                    'base': (0, 1),
                    'current': ((vector_current - vector_previous)[0], (vector_current - vector_previous)[1])
                }
            }
        }
        signals = controller.calculate_control_signals(
            centers, object_list, {'thief': (1, 2)}, sensors)
        alpha = int(signals[0]['param'])
        print('alpha is {}'.format(alpha))
        if alpha > 50:
            controller.robot_client.rotate(alpha)

        if len(object_list) > 0:
            for key, value in object_list.items():
                height, width = image.shape[0], image.shape[1]
                x = int(value['center'][0] * width)
                y = int(value['center'][1] * height)
                cv2.circle(image, (x, y), 10, (255, 0, 0), -1)
        height, width = image.shape[0], image.shape[1]
        x = int(centers[1][0] * width)
        y = int(centers[1][1] * height)
        cv2.circle(image, (x, y), 10, (255, 255, 255), -1)
        cv2.imshow(window_name, image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        vector_previous = vector_current
    print('done')
    cv2.destroyAllWindows()
