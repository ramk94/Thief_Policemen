from camera_system import get_image
from object_detector import Detector
from strategy import Strategy
from graph_builder import GraphBuilder
from control_system import Controller

weight_path = ''
config_path = ''


class Game:
    """
    """

    def __init__(self, weight_path, config_path):
        self.gaming_board_image = get_image()

        self.detector = Detector()
        detector.load(weight_path, config_path)

        self.centers = detector.detect_gaming_board(gaming_board_image)

        self.graph_builder = GraphBuilder(self.centers)

        self.strategy = Strategy()

        self.controller = Controller()

    def is_over(self):
        """
        """
        return False

    def forward(self):
        """
        """
        image = get_image()

        object_list = self.detector.detect_objects(image)

        graph, objects_on_graph = self.graph_builder.build(object_list)

        instructions = self.strategy.get_next_steps(graph, objects_on_graph)

        while not self.controller.is_finished(centers, object_list, instructions):
            control_signals = self.controller.calculate_control_signals(
                centers, object_list, instructions)
            self.controller.move_robots(control_signals)

            image = get_image()
            object_list = self.detector.detect_objects(image)

    def report(self):
        """
        """


if __name__ == '__main__':
    game = Game(weight_path, config_path)
    while not game.is_over():
        game.forward()
    game.report()
