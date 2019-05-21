import numpy as np


class GraphBuilder:
    """
    Graph builder which maintains gaming board's information and builds graphs based on robots' locations.
    """

    def __init__(self, centers):
        """
        Load gaming board information.

        Parameters
        ----------
        centers: list
            centers' coordinates of triangles on the gaming board
        """
        self.centers = centers

    def build(self, object_list):
        """
        Build a graph based on object list.

        Parameters
        ----------
        object_list: dict
            objects' relative locations, relative sizes and categories

        Returns
        ----------
        graph: numpy array
            N * N matrix which describes a graph
        objects_on_graph: dict
            a dict which indicates robots' locations on the graph
        """
        num_nodes = len(centers)
        graph = np.zeros((num_nodes, num_nodes), dtype=np.int64)
        objects_on_graph = {
            'thief': 3,
            'policeman1': 7,
            'policeman2': 9
        }
        return graph, objects_on_graph
