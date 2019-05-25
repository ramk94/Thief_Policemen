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
 
        sample_graph = [
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

        self.object_list = object_list;
        graph = np.array(sample_graph, dtype=np.int64)
        num_nodes = len(self.centers)
        assert num_nodes == graph.shape[0] and num_nodes == graph.shape[1]

        #objects_on_graph = {}

        #for key,value in self.object_list.items():
        #    if value[2] !=None:
        #        objects_on_graph[value[2]]=key;
        self.objects_on_graph = self.update_objects_on_graph()

        return graph, self.objects_on_graph

    #Update if the objects have moved from one location to the other
    #Need old node and current node to update the information
    #Update the size of the object, thief, police have different sizes
    def update_objects(self,old_node, new_node, new_object,new_size):
        self.object_list[old_node][2]=None
        self.object_list[new_node][2]=new_object
        self.object_list[old_node][1]=(None,None);
        self.object_list[new_node][1]=(new_size);
        self.objects_on_graph = self.update_objects_on_graph()


    def print_objectlist(self):
        for key,val in self.object_list.items():
            print("\nNode: ",key)
            print("Center information: ",val[0])
            print("Size information  : ",val[1])
            print("Object on graph   : ",val[2])
        print("\nObjects on Graph after the update: ",self.objects_on_graph);

    def update_objects_on_graph(self):
        objects_on_graph = {}
        for key,value in self.object_list.items():
            if value[2] !=None:
                objects_on_graph[value[2]]=key;
        return objects_on_graph;


