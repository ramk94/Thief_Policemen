import numpy as np


class GraphBuilder:
    """
    """

    def __init__(self, centers):
        """
        """
        self.centers = centers

    def build(self, object_list):
        """
        """
        num_nodes = len(centers)
        graph = np.zeros((num_nodes, num_nodes))
        objects_on_graph = {
            'thief': 3,
            'policeman1': 7,
            'policeman2': 9
        }
        return graph, objects_on_graph
