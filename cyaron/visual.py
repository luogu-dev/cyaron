from .graph import * 
import pygraphviz as pgv

def visualize(graph, **kwargs):
    """visualize(graph, **kwargs) -> None
        Graph graph -> the graph that will be visualized
        **kwargs(Keyword args):
            string outptu_file -> the path of the image
    """
    output_file = kwargs.get("output_file", "a.png")
    G = pgv.AGraph(directed=graph.directed)

    G.add_nodes_from([i for i in xrange(1, len(graph.edges))])
    for edge in graph.iterate_edges():
        G.add_edge(edge.start, edge.end, label=edge.weight)
        
    G.node_attr['shape'] = 'egg'
    G.node_attr['width'] = '0.25'
    G.node_attr['height'] = '0.25'
    G.edge_attr['arrowhead'] = 'open'

    G.layout(prog='dot')
    G.draw(output_file)
    

