import unittest
from camera_system import Camera
from object_detector import Detector


class TestCameraSystem(unittest.TestCase):

    def test_object_boxes(self):
        camera_raw = Camera('../data/videos/2019-06-01.avi', save=False, num_skip=0, draw=False)
        camera_labeled = Camera(None, save=False, window_name='labeled')
        weight_path = '../model/custom_tiny_yolov3.weights'
        network_config_path = '../cfg/custom-tiny.cfg'
        object_config_path = '../cfg/custom.data'
        detector = Detector(weight_path, network_config_path, object_config_path, auto_id=True)
        while True:
            image = camera_raw.get_image()
            if image is None:
                break
            image = camera_raw.rgb_to_bgr(image)
            object_list = detector.detect_objects(image)
            boxes = camera_raw.draw_boxes(image, object_list)
            camera_labeled.display(boxes)
        del camera_raw
        del camera_labeled


if __name__ == '__main__':
    unittest.main()
