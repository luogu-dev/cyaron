from .graph import *

class Merger:
    def __init__(self, *graphs, **kwargs):
        """__init__(self, *graphs, **kwargs) -> None
            put several graphs into one
            list graphs -> the graphs that will be merged
            list kwargs:
                None
        """
        self.graphs = graphs
        self.G = Graph(sum([len(i.edges) - 1 for i in graphs]), graphs[0].directed)
    
        counter = 0 
        for graph in self.graphs:
            graph.offset = counter
            for edge in graph.iterate_edges():
                self.G.add_edge(edge.start + counter, 
                                edge.end + counter, 
                                weight=edge.weight)
            counter += len(graph.edges) - 1

    def __add_edge(self, u, v, **kwargs):
        """__add_edge(self, u, v, **kwargs)
            tuple u -> (graph_index, vertex) indicating the start point
            tuple v -> (graph_index, vertex) indicating the end point
            **kwargs:
                int weight -> edge weight
        """
        self.G.add_edge(self.graphs[ u[0] ].offset + u[1],
                        self.graphs[ v[0] ].offset + v[1], 
                        weight=kwargs.get("weight", 1)) 
    
    def add_edge(self, u, v, **kwargs):
        """add_edge(self, u, v, **kwargs) -> None
        """
        self.__add_edge(u, v, **kwargs)

    def to_str(self, **kwargs):
        return self.G.to_str(**kwargs)
    
    def __str__(self):
        return self.to_str()

    @staticmethod
    def component(point_count, edge_count, **kwargs):
        """component(point_count, edge_count, **kwargs)
            generate a graph with certain components
            int point_count -> the number of vertices of each component
            int edge_count -> the number of edges of each component
            **kwargs:
                int component_count -> indicating how many components there are
        """
        component_count = kwargs.get("component_count", (2, 2))
        if not list_like(component_count):
            component_count = (component_count, component_count)
        real_count = random.randint(*component_count)
        graphs = [None] * real_count
        for i in xrange(real_count):
            graphs[i] = Graph.graph(point_count, edge_count, **kwargs)
        G = Merger(*graphs)
        return G.G
