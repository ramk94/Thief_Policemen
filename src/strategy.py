import numpy as np
import random
from collections import defaultdict
from heapq import *
import sys
from gesture_control import GestureControl
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)
inf = sys.maxsize  # inf


class Strategy:
    """
    Strategy module which make decisions for robots' future movements.
    """

    def __init__(self, orders):
        self.orders = orders
        self.fixed = []
        self.gesture_detector = GestureControl()

    @staticmethod
    def gesture_converter(graph, object_locations, robot, gesture):
        """
        Convert a gesture to an instruction on the object graph

        :param graph:
        :param object_locations:
        :param robot:
        :param gesture:
        :return:
        """
        # Palm: left
        # Fist: right
        # Swing: bottom
        # None: stay at the same place

        gestures = ['Palm', 'Fist', 'Swing', 'None']
        gestures_fake = ['left', 'right', 'bottom', 'None']
        assert gesture in gestures or gesture in gestures_fake
        current_location = object_locations[robot]
        max_nodes = graph.shape[0]
        level = 1
        lower_bound = level ** 2 - 2 * level + 2
        upper_bound = level ** 2
        while not (current_location >= lower_bound and current_location <= upper_bound):
            level += 1
            lower_bound = level ** 2 - 2 * level + 2
            upper_bound = level ** 2
        left = current_location - 1
        right = current_location + 1
        is_valid = True
        if lower_bound % 2 == 0:
            if current_location % 2 == 0:
                bottom = current_location + level * 2
            else:
                bottom = current_location - (level - 1) * 2
        else:
            if current_location % 2 == 0:
                bottom = current_location - (level - 1) * 2
            else:
                bottom = current_location + level * 2
        if gesture == gestures[0] or gesture == gestures_fake[0]:
            next_step = left
            if left < lower_bound:
                is_valid = False
        elif gesture == gestures[1] or gesture == gestures_fake[1]:
            next_step = right
            if right > upper_bound:
                is_valid = False
        elif gesture == gestures[2] or gesture == gestures_fake[2]:
            next_step = bottom
            if bottom > max_nodes:
                is_valid = False
        else:
            next_step = current_location

        if not is_valid:
            next_step = current_location
        return is_valid, next_step

    def get_next_steps_shortest_path(self, graph, objects_on_graph):

        instructions = {}
        object_locations = objects_on_graph.copy()

        target = 'thief'
        chasing_group = set(self.orders)
        if target in chasing_group:
            chasing_group.remove(target)
        for current_robot in self.orders:
            if current_robot == target:
                input('Press ENTER to recognize a gesture:')
                # gesture=input('input a gesture:')
                gesture = self.gesture_detector.get_gesture()
                # gesture=input()
                logger.info('current gesture is {}'.format(gesture))
                is_valid, instruction = self.gesture_converter(graph, objects_on_graph, target, gesture)
                counter = 3
                while not is_valid or counter == 0:
                    input('Invalid movement. Press ENTER to recognize a gesture again:')
                    # gesture = input('input a gesture:')
                    gesture = self.gesture_detector.get_gesture()
                    logger.info('current gesture is {}'.format(gesture))
                    is_valid, instruction = self.gesture_converter(graph, objects_on_graph, target, gesture)
                    counter -= 1
                if counter == 0:
                    logger.warning('Tried too many times, stay at the same node.')
                instructions[target] = [object_locations[target], instruction]
            else:
                robot_graph = graph.copy()
                block_indices = [object_locations[block] - 1 for block in chasing_group.difference({current_robot})]
                robot_graph[object_locations[current_robot] - 1][block_indices] = inf
                shortest = self.dijkstra(robot_graph, object_locations[current_robot] - 1, object_locations[target] - 1)
                if len(shortest) >= 2:
                    instructions[current_robot] = [object_locations[current_robot], shortest[1] + 1]
                else:
                    instructions[current_robot] = [object_locations[current_robot], object_locations[current_robot]]
                object_locations[current_robot] = instructions[current_robot][1]

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
    while True:
        thief_step = input('Input a gesture: ')
        valid, thief_next = Strategy.gesture_converter(graph, objects_on_graph, 'thief', thief_step)
        instructions = S1.get_next_steps_shortest_path(graph, objects_on_graph)
        instructions['thief'] = [objects_on_graph['thief'], thief_next]
        print(instructions)
        for p in ['policeman1', 'policeman2']:
            objects_on_graph[p] = instructions[p][1]
        objects_on_graph['thief'] = thief_next
