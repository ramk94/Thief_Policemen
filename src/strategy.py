import numpy as np
import random
from collections import defaultdict
from heapq import *

inf = 999999  # inf


class Strategy:
    """
    Strategy module which make decisions for robots' future movements.
    """

    def __init__(self, orders):
        self.orders = orders
        self.fixed = ['policeman1', 'policeman2']

    def get_next_step2_2(self, graph, objects_on_graph):
        instructions = {}

        current_objects_on_graph = objects_on_graph.copy()

        current_graph_police1 = graph.copy()
        current_graph_police1[current_objects_on_graph['policeman1'] - 1][
            current_objects_on_graph['policeman2'] - 1] = inf
        path_p1 = self.dijkstra(current_graph_police1, current_objects_on_graph['policeman1'] - 1,
                                current_objects_on_graph['thief'] - 1)
        if len(path_p1) >= 2:
            instructions['policeman1'] = [current_objects_on_graph['policeman1'], path_p1[1] + 1]
        else:
            instructions['policeman1'] = [current_objects_on_graph['policeman1'],
                                          current_objects_on_graph['policeman1']]
        current_objects_on_graph['policeman1'] = instructions['policeman1'][1]

        current_graph_police2 = graph.copy()
        current_graph_police2[current_objects_on_graph['policeman2'] - 1][
            current_objects_on_graph['policeman1'] - 1] = inf
        path_p2 = self.dijkstra(current_graph_police2, current_objects_on_graph['policeman2'] - 1,
                                current_objects_on_graph['thief'] - 1)
        if len(path_p2) >= 2:
            instructions['policeman2'] = [current_objects_on_graph['policeman2'], path_p2[1] + 1]
        else:
            instructions['policeman2'] = [current_objects_on_graph['policeman2'],
                                          current_objects_on_graph['policeman2']]

        current_objects_on_graph['policeman2'] = instructions['policeman2'][1]

        return instructions

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
        for name in self.fixed:
            if name in instructions:
                instructions[name][1] = instructions[name][0]
        return instructions

    def dijkstra_raw(self, edges, from_node, to_node):
        g = defaultdict(list)
        for l, r, c in edges:
            g[l].append((c, r))
        q, seen = [(0, from_node, ())], set()
        while q:
            (cost, v1, path) = heappop(q)
            if v1 not in seen:
                seen.add(v1)
                path = (v1, path)
                if v1 == to_node:
                    return cost, path
                for c, v2 in g.get(v1, ()):
                    if v2 not in seen:
                        heappush(q, (cost + c, v2, path))
        return float("inf"), []

    def dijkstra(self, matrix, from_node, to_node):
        matrix[matrix == 0] = inf
        edges = []
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if i != j and matrix[i][j] != inf:
                    edges.append((i, j, matrix[i][j]))
        ret_path = []
        length, path_queue = self.dijkstra_raw(edges, from_node, to_node)
        if len(path_queue) > 0:
            left = path_queue[0]
            ret_path.append(left)
            right = path_queue[1]
            while len(right) > 0:
                left = right[0]
                ret_path.append(left)
                right = right[1]
            ret_path.reverse()
        return ret_path


if __name__ == '__main__':
    example = [
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

    graph = np.array(example, dtype=np.int64)

    thief_path = [13, 14, 15, 16]
    S1 = Strategy(['thief', 'policeman1', 'policeman2'])
    objects_on_graph = {
        'thief': 7,
        'policeman1': 2,
        'policeman2': 4
    }
    instructions = S1.get_next_step2_2(graph, objects_on_graph)
    print(instructions)
    for thief_step in thief_path:
        objects_on_graph['policeman1'] = instructions['policeman1'][1]
        objects_on_graph['policeman2'] = instructions['policeman2'][1]
        objects_on_graph['thief'] = thief_step
        instructions = S1.get_next_step2_2(graph, objects_on_graph)
        print(instructions)
