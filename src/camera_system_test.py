import unittest
from camera_system import Camera


class TestCameraSystem(unittest.TestCase):
    def test_video_stream(self):
        camera = Camera('../data/videos/2019-06-01.avi', save=False, num_skip=0)
        while camera.get_image() is not None:
            pass
        del camera


if __name__ == '__main__':
    unittest.main()
