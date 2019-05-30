import numpy as np
import logging

logger = logging.getLogger(__name__)


class Controller:
    """
    Control system is the most important part of our project.
    """

    def calculate_control_signals(self, centers, object_list, instructions):
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
                centers[instructions[key][1]]).reshape((-1, 1))

            # calculate the angle between centers
            delta = next_center - current_center
            cos_theta = (base_unit_vector.T @ delta) / np.linalg.norm(delta)
            theta = np.arccos(cos_theta)

            # calculate the angle between orientations
            alpha = np.arccos(base_unit_vector.T @ current_direction)

            # calculate rotate angle
            gamma = (alpha-theta)/np.pi*360

            # construct rotate signal
            signals.append({
                'name': key,
                'type': 'rotate',
                'param': gamma
            })

            # construct move signal
            signals.append({
                'name': key,
                'type': 'move',
                'param': 1
            })
        return signals

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
                            'base': (1, 2, 3),
                            'current': (2, 4, 1.5)
                        }
                    },
                    'policeman1': {
                        'orientation': {
                            'base': (1, 2, 3),
                            'current': (2, 4, 1.5)
                        }
                    },
                    'policeman2': {
                        'orientation': {
                            'base': (1, 2, 3),
                            'current': (2, 4, 1.5)
                        }
                    }
                }
        """
        sensor_data = {
            'thief': {
                'orientation': {
                    'base': (1, 2, 3),
                    'current': (2, 4, 1.5)
                }
            },
            'policeman1': {
                'orientation': {
                    'base': (1, 2, 3),
                    'current': (2, 4, 1.5)
                }
            },
            'policeman2': {
                'orientation': {
                    'base': (1, 2, 3),
                    'current': (2, 4, 1.5)
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
            if np.linalg.norm(current_center-target_center) <= threshold:
                logger.info('{0} has moved to node {1}.'.format(key, target))
            else:
                is_done = False
                logger.info(
                    '{0} has not moved to node {1}.'.format(key, target))
        return is_done
