from graph_builder import GraphBuilder

#Contains center information for nine locations
centers = [
            (0.1, 0.6),
            (0.2, 0.2),
            (0.2, 0.4),
            (0.2, 0.8),
            (0.6, 0.2),
            (0.6, 0.5),
            (0.6, 0.6),
            (0.6, 0.7),
            (0.7, 0.9),
        ]

#Contains information of relative locations, relative sizes and categories
object_list = {"1":[[(centers[0][0],centers[0][1])],[(0.8,0.9)],"thief"],
               "2":[[(centers[1][0],centers[1][1])],[(None,None)],None],
               "3":[[(centers[2][0],centers[2][1])],[(None,None)],None],
               "4":[[(centers[3][0],centers[3][1])],[(None,None)],None],
               "5":[[(centers[4][0],centers[4][1])],[(0.3,0.3)],"police1"],
               "6":[[(centers[5][0],centers[5][1])],[(None,None)],None],
               "7":[[(centers[6][0],centers[6][1])],[(None,None)],None],
               "8":[[(centers[7][0],centers[7][1])],[(None,None)],None],
               "9":[[(centers[8][0],centers[8][1])],[(0.3,0.3)],"police2"]
               }



#Test the graphBuilder
objtest = GraphBuilder(centers);

graph,objects_on_graph = objtest.build(object_list);
print(graph)
print(objects_on_graph)
print("\n\n\n")

objtest.update_objects("1","4","thief",(0.8,0.9))
objtest.print_objectlist()
