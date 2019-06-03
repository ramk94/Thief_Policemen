import numpy as np
import random


class Strategy:
    """
    Strategy module which make decisions for robots' future movements.
    """

    def __init__(self, orders):
        self.orders = orders

    def get_next_step2_2(self, graph, objects_on_graph):
        pass

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
        current_objects_on_graph = objects_on_graph.copy()

        for name in self.orders:
            # set up graph
            current_graph = graph.copy()
            for value in current_objects_on_graph.values():
                current_graph[:, value - 1] = 0

            # find next step
            if name in current_objects_on_graph:
                item_index_1 = np.where(
                    current_graph[current_objects_on_graph[name] - 1, :] == 1)
                item_index_2 = np.where(
                    current_graph[:, current_objects_on_graph[name] - 1] == 1)
                choices = list(set(item_index_1[0]) | set(item_index_2[0]))
                if len(choices) == 0:
                    instructions[name] = [current_objects_on_graph[name], current_objects_on_graph[name]]
                else:
                    next_step = random.choice(choices)
                    instructions[name] = [current_objects_on_graph[name], next_step + 1]
                    current_objects_on_graph[name] = next_step + 1
        return instructions


if __name__ == '__main__':
    # example = [
    #     [0, 0, 1, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 1, 0, 0, 1, 0, 0, 0],
    #     [1, 1, 0, 1, 0, 0, 0, 0, 0],
    #     [0, 0, 1, 0, 0, 0, 0, 1, 0],
    #     [0, 0, 0, 0, 0, 1, 0, 0, 0],
    #     [0, 1, 0, 0, 1, 0, 1, 0, 0],
    #     [0, 0, 0, 0, 0, 1, 0, 1, 0],
    #     [0, 0, 0, 1, 0, 0, 1, 0, 1],
    #     [0, 0, 0, 0, 0, 0, 0, 1, 0]
    # ]
    example = [
        [0, 0, 1, 0],
        [0, 0, 1, 0],
        [1, 1, 0, 1],
        [0, 0, 1, 0]
    ]
    graph = np.array(example, dtype=np.int64)
    objects_on_graph = {
        'policeman1': 3,
        'policeman2': 4
    }
    S1 = Strategy(['thief', 'policeman1', 'policeman2'])
    print(S1.get_next_steps(graph, objects_on_graph))
