from camera_system import Camera
from object_detector import Detector
from strategy import Strategy
from graph_builder import GraphBuilder
from control_system import Controller
import logging
import sys

WEIGHT_PATH = '../model/custom_tiny_yolov3.weights'
NETWORK_CONFIG_PATH = '../cfg/custom-tiny.cfg'
OBJECT_CONFIG_PATH = '../cfg/custom.data'
ROBOTS_CONFIG_PATH = '../cfg/robots.json'

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)


class Game:
    """
    Each game is an instance of class Game.
    """

    def __init__(self, weight_path, network_config_path, object_config_path, robots_config_path):
        """
        Load necessary modules and files.

        Parameters
        ----------
        weight_path: str
            file path of YOLOv3 network weights
        config_path: str
            file path of YOLOv3 network configurations
        """
        self.orders = ['thief', 'policeman1', 'policeman2']

        # construct the camera system
        self.camera = Camera()

        # construct the object detector
        self.detector = Detector(
            weight_path, network_config_path, object_config_path)

        # load gaming board image and get centers' coordinates of triangles
        self.gaming_board_image = self.camera.get_image()
        self.centers = self.detector.detect_gaming_board(
            self.gaming_board_image)

        # construct the graph builder
        self.graph_builder = GraphBuilder(self.centers)

        # construct the strategy module
        self.strategy = Strategy(self.orders)

        # construct the control system
        self.controller = Controller(self.detector, self.camera.get_image, robots_config_path)
        self.controller.connect()

    def is_over(self):
        """
        Check if the game is over.

        Returns
        -------
        game_over: bool
            True if the thief is at the escape point or the policemen have caught the thief, otherwise False.
        """
        game_over = False
        return game_over

    def forward(self):
        """
        Push the game to the next step.
        """
        # get objects' coordinates and categories
        image = self.camera.get_image()
        object_list = self.detector.detect_objects(image)

        # build a graph based on object list
        graph, objects_on_graph = self.graph_builder.build(object_list)

        # generate instructions based on the graph
        instructions = self.strategy.get_next_steps(graph, objects_on_graph)
        logger.info('instructions:{}'.format(instructions))
        # move robots until they reach the right positions
        while not self.controller.is_finished(self.centers, object_list, instructions):
            # obtain feedback from camera
            image = self.camera.get_image(save=True)
            object_list = self.detector.detect_objects(image)

            # calculate control signals
            control_signals = self.controller.calculate_control_signals(
                self.centers, object_list, instructions)

            # cut extra signals
            real_signals = []
            for name in self.orders:
                for signal in control_signals:
                    if signal['name'] == name:
                        real_signals.append(signal)
                if len(real_signals) > 0:
                    break

            # update internal states
            self.controller.update_state(object_list)

            # move robots
            self.controller.move_robots(real_signals)

            # obtain feedback from camera
            image = self.camera.get_image(save=True)
            object_list = self.detector.detect_objects(image)

            # update internal states
            self.controller.update_state(object_list)

    def get_report(self):
        """
        Generate a game report(json, xml or plain text).

        Returns
        -------
        game_report: object or str
            a detailed record of the game
        """
        game_report = None
        return game_report


if __name__ == '__main__':
    # construct a game
    input('Press ENTER to start a game:')
    game = Game(WEIGHT_PATH, NETWORK_CONFIG_PATH,
                OBJECT_CONFIG_PATH, ROBOTS_CONFIG_PATH)

    # keep running until the game is over
    while not game.is_over():
        # input('Press ENTER to the next game step:')
        game.forward()

    # obtain and print the game report
    input('The game is over. Press ENTER to the print a game report:')
    report = game.get_report()
    print(report)
