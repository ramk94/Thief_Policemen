import numpy as np
import random
class Strategy:
    """
    Strategy module which make decisions for robots' future movements.
    """

    def get_next_steps(self, graph, objects_on_graph):

        """
        Make decisions for robots.

        Parameters
        ----------
        graph: numpy array
            N * N matrix which describes a graph
        objects_on_graph: dict
            a dict which indicates robots' locations on the graph

        Returns
        -------
        instructions: dict
            a dict consists of future decisions
        """
        instructions = {}
        for object in objects_on_graph:
            #print(graph[:, objects_on_graph[object] - 1])
            item_index_1 = np.where(graph[objects_on_graph[object] - 1, :] == 1)
            item_index_2 = np.where(graph[:, objects_on_graph[object] - 1] == 1)
            choices = list(set(item_index_1[0]) | set(item_index_2[0]))
            next_step = random.choice(choices)
            instructions[object] = [objects_on_graph[object], next_step]
        #instructions = {
        #    'thief': (3, 4),
        #    'policeman1': (7, 6),
        #    'policeman2': (9, 8)
        #}
        return instructions


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
S1 = Strategy()
print(S1.get_next_steps(graph, objects_on_graph))