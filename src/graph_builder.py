import numpy as np
import math


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
        self.center_dict = self.center_info()

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
        graph_4 = [
            [0, 0, 1, 0],
            [0, 0, 1, 0],
            [1, 1, 0, 1],
            [0, 0, 1, 0]
        ]
        graph_9 = [
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
        graph_16 = [
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
        ]
        num_nodes = len(self.centers)
        if num_nodes == 4:
            sample_graph = graph_4
        elif num_nodes == 9:
            sample_graph = graph_9
        elif num_nodes == 16:
            sample_graph = graph_16
        else:
            raise Exception('wrong center number {}'.format(num_nodes))

        self.object_list = object_list
        graph = np.array(sample_graph, dtype=np.int64)
        assert num_nodes == graph.shape[0] and num_nodes == graph.shape[1]

        self.objects_on_graph = self.objects_ongraph()

        return graph, self.objects_on_graph

    # Function that returns the current center object
    # Uses euclidian distance formula to make the prediction of the object current location
    def return_current_center(self, p2, q2):
        closest = {}
        smallest = 0
        for center in self.centers:
            q1 = center[1]
            p1 = center[0]
            smallest = math.sqrt((q2 - q1) ** 2 + (p2 - p1) ** 2)
            closest[smallest] = (p1, q1)

        smallest = min(closest.keys())

        # objects_on_graph = {}
        ''' Example
        object_list{
                    "thief":{
                              "center":(0.16.0.37)
                            },
                    "police1":{
                            {
                              "center": (0.2,0.4)
                            }
                    "police2":{
                              "center": (0.4,0.5)
                              }
                   }
        '''
        return closest[smallest]

    # From the original center info, put them in dictionary for future lookup
    def center_info(self):
        center_dict = {}
        i = 1
        for val in self.centers:
            center_dict[val] = i
            i = i + 1

        return center_dict

    # Function that returns a dictionary of objects that are currently occupying the space
    def objects_ongraph(self):
        objects_on_graph = {}
        for key, value in self.object_list.items():
            current_val = value["center"]
            current_center = self.return_current_center(current_val[0], current_val[1])
            objects_on_graph[key] = self.center_dict[current_center]
        return objects_on_graph
