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
            example:
                Assume we have nine nodes on the gaming board, and we already know the center coordinate of each node.
                Then an output graph(numpy array) format may like the array below, and you can find the image of this
                example in Thief_Policemen/resources/examples/gaming_board_graph.JPG
                [  # 1 2 3 4 5 6 7 8 9
                    [0,0,1,0,0,0,0,0,0],
                    [0,0,1,0,0,1,0,0,0],
                    [1,1,0,1,0,0,0,0,0],
                    [0,0,1,0,0,0,0,1,0],
                    [0,0,0,0,0,1,0,0,0],
                    [0,1,0,0,1,0,1,0,0],
                    [0,0,0,0,0,1,0,1,0],
                    [0,0,0,1,0,0,1,0,1],
                    [0,0,0,0,0,0,0,1,0]
                ]
        objects_on_graph: dict
            a dict which indicates robots' locations on the graph
            example:
                Assume thief is at node #3, policeman1 is at node #7 and policeman2 is at node #9, then this dict may like
                the dict below.
                {
                    "thief": 3,
                    "policeman1": 7,
                    "policeman2": 9
                }
        """
        example = [
            [0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 1, 0, 0, 0],
            [1, 1, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 0, 1, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 1, 0],
            [0, 0, 0, 1, 0, 0, 1, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 1, 0]
        ]
        graph = np.array(example, dtype=np.int64)
        objects_on_graph = {
            'thief': 3,
            'policeman1': 7,
            'policeman2': 9
        }
        num_nodes = len(self.centers)
        assert num_nodes == graph.shape[0] and num_nodes == graph.shape[1]
        return graph, objects_on_graph
