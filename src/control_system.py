class Controller:
    """
    Control system is the most important part of our project.
    """

    def calculate_control_signals(self, centers, object_list, instructions):
        """
        calculate real control signals based on instructions.

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
        sensor_data = self.get_sensor_data()
        signals = []
        return signals

    def get_sensor_data(self):
        """
        Collect senor data from robots.

        Returns
        -------
        sensor_data: dict
            sensor data like orientations
        """
        sensor_data = {
            'thief': None,
            'policeman1': None,
            'policeman2': None
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

    def is_finished(self, centers, object_list, instructions):
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
        return is_done
