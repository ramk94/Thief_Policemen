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
object_list = {
             "thief":{
                        "center":(0.5,0.7)
                      },
             "police1":{
                       
                          "center": (0.6,0.2)
                       },
             "police2":{
                           "center": (0.7,0.9)
                        }
            }



#Test the graphBuilder
objtest = GraphBuilder(centers);

graph,objects_on_graph = objtest.build(object_list);
print(graph)
print(objects_on_graph)
print("\n\n\n")

