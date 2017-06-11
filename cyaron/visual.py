from .graph import * 
from .merger import Merger
import pygraphviz as pgv

def visualize(graph, output_path="a.png"):
    """visualize(graph, **kwargs) -> None
        Graph/Merger graph -> the graph/Merger that will be visualized
        string output_path-> the output path of the image
    """

    if isinstance(graph, Merger): graph = Merger.G
    G = pgv.AGraph(directed=graph.directed)

    G.add_nodes_from([i for i in xrange(1, len(graph.edges))])
    for edge in graph.iterate_edges():
        G.add_edge(edge.start, edge.end, label=edge.weight)
        
    G.node_attr['shape'] = 'egg'
    G.node_attr['width'] = '0.25'
    G.node_attr['height'] = '0.25'
    G.edge_attr['arrowhead'] = 'open'

    G.layout(prog='dot')
    G.draw(output_path)
    

