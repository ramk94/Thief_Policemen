class Detector:
    """
    YOLO detector
    """

    def load(self, weight_path, config_path):
        """
        load YOLO network weights and config files
        """

    def detect_objects(self, image):
        """
        input: image
        output: objects' relative locations, relative sizes and categories
        """
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
        input: image
        output: center relative coordinate of triangles on the gaming board
        """
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
