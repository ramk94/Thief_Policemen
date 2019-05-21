class Detector:
    """
    Object detector based on YOLO network.
    """

    def load(self, weight_path, config_path):
        """
        Load YOLO network weights and config files

        Parameters
        ----------
        weight_path: str
            file path of YOLOv3 network weights
        config_path: str
            file path of YOLOv3 network configurations
        """

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
