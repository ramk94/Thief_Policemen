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
        instructions = {
            'thief': (3, 4),
            'policeman1': (7, 6),
            'policeman2': (9, 8)
        }
        return instructions
