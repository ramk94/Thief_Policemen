from camera_system import get_image
from object_detector import Detector
from strategy import Strategy
from graph_builder import GraphBuilder
from control_system import Controller

weight_path = ''
config_path = ''

if __name__ == '__main__':
    gaming_board_image = get_image()
    detector = Detector()
    detector.load(weight_path, config_path)
    centers = detector.detect_gaming_board(gaming_board_image)
    graph_builder = GraphBuilder(centers)
    strategy = Strategy()
    controller = Controller()
    while True:
        image = get_image()
        object_list = detector.detect_objects(image)
        graph = graph_builder.build(object_list)
        instructions = strategy.get_next_steps(graph)
        control_signals = controller.calculate_control_signals(
            centers, object_list, instructions)
        controller.move_robots(control_signals)
