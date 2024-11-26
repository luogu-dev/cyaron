from .utils import *
from .vector import Vector
import random
from typing import TypeVar, Callable

__all__ = ["Edge", "Graph"]


class Edge:
    """Class Edge: A class of the edge in the graph"""

    def __init__(self, u, v, w):
        """__init__(self, u, v, w) -> None
            Initialize a edge. 
            int u -> the start vertex
            int v -> the end vertex
            int w -> the weight.
        """
        self.start = u
        self.end = v
        self.weight = w

    def __str__(self):
        """__str__(self) -> str
            Return a string to output the edge. The string contains the start vertex, end vertex and weight(u,v,w) and splits with space.
        """
        return "%d %d %d" % (self.start, self.end, self.weight)

    @staticmethod
    def unweighted_edge(edge):
        """unweighted_edge(edge) -> str
            Return a string to output the edge without weight. The string contains the start vertex, end vertex(u,v) and splits with space.
        """
        return '%d %d' % (edge.start, edge.end)


class Graph:
    """Class Graph: A class of the graph
    """

    def __init__(self, point_count, directed=False):
        """__init__(self, point_count) -> None
            Initialize a graph.
            int point_count -> the count of the vertexes in the graph.
            bool directed = False -> whether the graph is directed(true:directed,false:not directed)
        """
        self.directed = directed
        self.edges = [[] for i in range(point_count + 1)]

    def edge_count(self):
        """edge_count(self) -> int
            Return the count of the edges in the graph.
        """
        cnt = sum(len(node) for node in self.edges)
        if not self.directed:
            cnt //= 2
        return cnt

    def to_matrix(self, **kwargs):
        """to_matrix(self, **kwargs) -> GraphMatrix
            Convert the graph to adjacency matrix.
            **kwargs(Keyword args):
                int default = -1 -> the default value when the edge does not exist.
                Any merge(Any, Edge)
                = lambda val, edge: edge.weight
                -> the mapping from the old values in matrix and the edges to the new values in matrix.
        """
        return GraphMatrix(self, **kwargs)

    def to_str(self, **kwargs):
        """to_str(self, **kwargs) -> str
            Convert the graph to string with format. Splits with "\n"
            **kwargs(Keyword args):
                bool shuffle = False -> whether shuffle the output or not
                str output(Edge) = str -> the convert function which converts object Edge to str. the default way is to use str()
        """
        shuffle = kwargs.get("shuffle", False)
        output = kwargs.get("output", str)
        buf = []
        if shuffle:
            new_node_id = [i for i in range(1, len(self.edges))]
            random.shuffle(new_node_id)
            new_node_id = [0] + new_node_id
            edge_buf = []
            for edge in self.iterate_edges():
                edge_buf.append(
                    Edge(new_node_id[edge.start], new_node_id[edge.end],
                         edge.weight))
            random.shuffle(edge_buf)
            for edge in edge_buf:
                if not self.directed and random.randint(0, 1) == 0:
                    (edge.start, edge.end) = (edge.end, edge.start)
                buf.append(output(edge))
        else:
            for edge in self.iterate_edges():
                buf.append(output(edge))
        return "\n".join(buf)

    def __str__(self):
        """__str__(self) -> str
            Return a string to output the graph. The string contains all the edges of the graph, splits with "\n".
        """
        return self.to_str()

    def iterate_edges(self):
        """iterate_edges(self) -> Edge
            Iter the graph. Order by the start vertex.
        """
        for node in self.edges:
            for edge in node:
                if edge.end >= edge.start or self.directed:
                    yield edge

    def __add_edge(self, x, y, w):
        """__add_edge(self, x, y, w) -> None
            Add an edge to the graph.
        """
        self.edges[x].append(Edge(x, y, w))

    def add_edge(self, x, y, **kwargs):
        """add_edge(self, x, y, **kwargs) -> None
            int x -> the start vertex
            int y -> the end vertex
            **kwargs(Keyword args):
                int weight = 1 -> the weight 
        """
        weight = kwargs.get("weight", 1)
        self.__add_edge(x, y, weight)
        if not self.directed and x != y:
            self.__add_edge(y, x, weight)

    @staticmethod
    def chain(point_count, **kwargs):
        """chain(point_count, **kwargs) -> Graph
               Factory method. Return a chain graph with point_count vertexes.
               int point_count -> the count of vertexes
               **kwargs(Keyword args):
                   bool directed = True -> whether the chain is directed(true:directed,false:not directed)
                   (int,int) weight_limit = (1,1) -> the limit of weight. index 0 is the min limit, and index 1 is the max limit(both included)
                   int weight_limit -> If you use a int for this arg, it means the max limit of the weight(included)
                   int/float weight_gen() 
                   = lambda: random.randint(weight_limit[0], weight_limit[1]) 
                   -> the generator of the weights. It should return the weight. The default way is to use the random.randint()
        """
        return Graph.tree(point_count, 1, 0, **kwargs)

    @staticmethod
    def flower(point_count, **kwargs):
        """flower(point_count, **kwargs) -> Graph
               Factory method. Return a flower graph with point_count vertexes.
               int point_count -> the count of vertexes
               **kwargs(Keyword args):
                   bool directed = True -> whether the chain is directed(true:directed,false:not directed)
                   (int,int) weight_limit = (1,1) -> the limit of weight. index 0 is the min limit, and index 1 is the max limit(both included)
                   int weight_limit -> If you use a int for this arg, it means the max limit of the weight(included)
                   int/float weight_gen() 
                   = lambda: random.randint(weight_limit[0], weight_limit[1]) 
                   -> the generator of the weights. It should return the weight. The default way is to use the random.randint()
        """
        return Graph.tree(point_count, 0, 1, **kwargs)

    @staticmethod
    def tree(point_count, chain=0, flower=0, **kwargs):
        """tree(point_count, chain=0, flower=0, **kwargs) -> Graph
               Factory method. Return a tree with point_count vertexes.
               int point_count -> the count of vertexes
               float chain = 0 -> 1 means the tree is a chain
               float flower = 0 -> 1 means the tree is a flower
               NOTICE:only either chain or flower can be True
               **kwargs(Keyword args):
                   bool directed = False -> whether the chain is directed(true:directed,false:not directed)
                   (int,int) weight_limit = (1,1) -> the limit of weight. index 0 is the min limit, and index 1 is the max limit(both included)
                   int weight_limit -> If you use a int for this arg, it means the max limit of the weight(included)
                   int/float weight_gen() 
                   = lambda: random.randint(weight_limit[0], weight_limit[1]) 
                   -> the generator of the weights. It should return the weight. The default way is to use the random.randint()
                   int father_gen(cur)
                   = lambda cur: random.randrange(1, cur)
                   -> the generator of the fathers of current point.
        """
        directed = kwargs.get("directed", False)
        weight_limit = kwargs.get("weight_limit", (1, 1))
        if not list_like(weight_limit):
            weight_limit = (1, weight_limit)
        weight_gen = kwargs.get(
            "weight_gen",
            lambda: random.randint(weight_limit[0], weight_limit[1]))
        father_gen = kwargs.get("father_gen",
                                lambda cur: random.randrange(1, cur))

        if not 0 <= chain <= 1 or not 0 <= flower <= 1:
            raise Exception("chain and flower must be between 0 and 1")
        if chain + flower > 1:
            raise Exception("chain plus flower must be smaller than 1")
        graph = Graph(point_count, directed)

        chain_count = int((point_count - 1) * chain)
        flower_count = int((point_count - 1) * flower)
        if chain_count > point_count - 1:
            chain_count = point_count - 1
        if chain_count + flower_count > point_count - 1:
            flower_count = point_count - 1 - chain_count
        random_count = point_count - 1 - chain_count - flower_count

        for i in range(2, chain_count + 2):
            graph.add_edge(i - 1, i, weight=weight_gen())
        for i in range(chain_count + 2, chain_count + flower_count + 2):
            graph.add_edge(1, i, weight=weight_gen())
        for i in range(point_count - random_count + 1, point_count + 1):
            u = father_gen(i)
            graph.add_edge(u, i, weight=weight_gen())

        return graph

    @staticmethod
    def binary_tree(point_count, left=0, right=0, **kwargs):
        """binary_tree(point_count, left=0, right=0, **kwargs) -> Graph
               Factory method. Return a binary tree with point_count vertexes.
               int point_count -> the count of vertexes
               float left = 0 -> random arg. should be in [0,1]
               float right = 0 -> random arg. should be in [0,1]
               NOTICE:left+right mustn't be greater than 1
               **kwargs(Keyword args):
                   bool directed = False -> whether the binary tree is directed(true:directed,false:not directed)
                   (int,int) weight_limit = (1,1) -> the limit of weight. index 0 is the min limit, and index 1 is the max limit(both included)
                   int weight_limit -> If you use a int for this arg, it means the max limit of the weight(included)
                   int/float weight_gen() 
                   = lambda: random.randint(weight_limit[0], weight_limit[1]) 
                   -> the generator of the weights. It should return the weight. The default way is to use the random.randint()
        """
        directed = kwargs.get("directed", False)
        weight_limit = kwargs.get("weight_limit", (1, 1))
        if not list_like(weight_limit):
            weight_limit = (1, weight_limit)
        weight_gen = kwargs.get(
            "weight_gen",
            lambda: random.randint(weight_limit[0], weight_limit[1]))

        if not 0 <= left <= 1 or not 0 <= right <= 1:
            raise Exception("left and right must be between 0 and 1")
        if left + right > 1:
            raise Exception("left plus right must be smaller than 1")

        can_left = [1]
        can_right = [1]
        graph = Graph(point_count, directed)
        for i in range(2, point_count + 1):
            edge_pos = random.random()
            node = 0
            # Left
            if edge_pos < left or left + right < edge_pos <= (1.0 - left -
                                                              right) / 2:
                point_index = random.randint(0, len(can_left) - 1)
                node = can_left[point_index]
                del_last_node = can_left.pop(
                )  # Save a copy of the last element
                if point_index < len(can_left):
                    # If the chosen element isn't the last one,
                    # Copy the last one to the position of the chosen one
                    can_left[point_index] = del_last_node
            # Right
            else:
                # elif left <= edge_pos <= left + right or (1.0 - left - right) / 2 < edge_pos < 1:
                point_index = random.randint(0, len(can_right) - 1)
                node = can_right[point_index]
                del_last_node = can_right.pop()
                if point_index < len(can_right):
                    can_right[point_index] = del_last_node
            graph.add_edge(node, i, weight=weight_gen())
            can_left.append(i)
            can_right.append(i)

        return graph

    @staticmethod
    def graph(point_count, edge_count, **kwargs):
        """graph(point_count, edge_count, **kwargs) -> Graph
               Factory method. Return a graph with point_count vertexes and edge_count edges.
               int point_count -> the count of vertexes
               int edge_count -> the count of edges
               **kwargs(Keyword args):
                   bool self_loop = True -> whether to allow self loops or not
                   bool repeated_edges = True -> whether to allow repeated edges or not
                   bool directed = False -> whether the chain is directed(true:directed,false:not directed)
                   (int,int) weight_limit = (1,1) -> the limit of weight. index 0 is the min limit, and index 1 is the max limit(both included)
                   int weight_limit -> If you use a int for this arg, it means the max limit of the weight(included)
                   int/float weight_gen() 
                   = lambda: random.randint(weight_limit[0], weight_limit[1]) 
                   -> the generator of the weights. It should return the weight. The default way is to use the random.randint()
        """
        directed = kwargs.get("directed", False)
        self_loop = kwargs.get("self_loop", True)
        repeated_edges = kwargs.get("repeated_edges", True)
        if not repeated_edges:
            max_edge = Graph._calc_max_edge(point_count, directed, self_loop)
            if edge_count > max_edge:
                raise Exception(
                    "the number of edges of this kind of graph which has %d vertexes must be less than or equal to %d."
                    % (point_count, max_edge))

        weight_limit = kwargs.get("weight_limit", (1, 1))
        if not list_like(weight_limit):
            weight_limit = (1, weight_limit)
        weight_gen = kwargs.get(
            "weight_gen",
            lambda: random.randint(weight_limit[0], weight_limit[1]))
        graph = Graph(point_count, directed)
        used_edges = set()
        i = 0
        while i < edge_count:
            u = random.randint(1, point_count)
            v = random.randint(1, point_count)

            if (not self_loop and u == v) or (not repeated_edges and
                                              (u, v) in used_edges):
                # Then we generate a new pair of nodes
                continue

            graph.add_edge(u, v, weight=weight_gen())

            if not repeated_edges:
                used_edges.add((u, v))
                if not directed:
                    used_edges.add((v, u))

            i += 1
        return graph

    @staticmethod
    def DAG(point_count, edge_count, **kwargs):
        """DAG(point_count, edge_count, **kwargs) -> Graph
               Factory method. Return a directed connected graph with point_count vertexes and edge_count edges.
               int point_count -> the count of vertexes
               int edge_count -> the count of edges
               **kwargs(Keyword args):
                   bool self_loop = False -> whether to allow self loops or not
                   bool repeated_edges = True -> whether to allow repeated edges or not
                   bool loop = False -> whether to allow loops or not
                   (int,int) weight_limit = (1,1) -> the limit of weight. index 0 is the min limit, and index 1 is the max limit(both included)
                   int weight_limit -> If you use a int for this arg, it means the max limit of the weight(included)
                   int/float weight_gen() 
                   = lambda: random.randint(weight_limit[0], weight_limit[1]) 
                   -> the generator of the weights. It should return the weight. The default way is to use the random.randint()
        """
        if edge_count < point_count - 1:
            raise Exception(
                "the number of edges of connected graph must more than the number of nodes - 1"
            )

        self_loop = kwargs.get("self_loop", False)  # DAG default has no loop
        repeated_edges = kwargs.get("repeated_edges", True)
        loop = kwargs.get("loop", False)
        if not repeated_edges:
            max_edge = Graph._calc_max_edge(point_count, not loop, self_loop)
            if edge_count > max_edge:
                raise Exception(
                    "the number of edges of this kind of graph which has %d vertexes must be less than or equal to %d."
                    % (point_count, max_edge))

        weight_limit = kwargs.get("weight_limit", (1, 1))
        if not list_like(weight_limit):
            weight_limit = (1, weight_limit)
        weight_gen = kwargs.get(
            "weight_gen",
            lambda: random.randint(weight_limit[0], weight_limit[1]))

        used_edges = set()
        edge_buf = list(
            Graph.tree(point_count, weight_gen=weight_gen).iterate_edges())
        graph = Graph(point_count, directed=True)

        for edge in edge_buf:
            if loop and random.randint(1, 2) == 1:
                edge.start, edge.end = edge.end, edge.start
            graph.add_edge(edge.start, edge.end, weight=edge.weight)

            if not repeated_edges:
                used_edges.add((edge.start, edge.end))

        i = point_count - 1
        while i < edge_count:
            u = random.randint(1, point_count)
            v = random.randint(1, point_count)

            if not loop and u > v:
                u, v = v, u

            if (not self_loop and u == v) or (not repeated_edges and
                                              (u, v) in used_edges):
                # Then we generate a new pair of nodes
                continue

            graph.add_edge(u, v, weight=weight_gen())

            if not repeated_edges:
                used_edges.add((u, v))

            i += 1

        return graph

    @staticmethod
    def UDAG(point_count, edge_count, **kwargs):
        """UDAG(point_count, edge_count, **kwargs) -> Graph
               Factory method. Return a undirected connected graph with point_count vertexes and edge_count edges.
               int point_count -> the count of vertexes
               int edge_count -> the count of edges
               **kwargs(Keyword args):
                   bool self_loop = True -> whether to allow self loops or not
                   bool repeated_edges = True -> whether to allow repeated edges or not
                   (int,int) weight_limit = (1,1) -> the limit of weight. index 0 is the min limit, and index 1 is the max limit(both included)
                   int weight_limit -> If you use a int for this arg, it means the max limit of the weight(included)
                   int/float weight_gen() 
                   = lambda: random.randint(weight_limit[0], weight_limit[1]) 
                   -> the generator of the weights. It should return the weight. The default way is to use the random.randint()
        """
        if edge_count < point_count - 1:
            raise Exception(
                "the number of edges of connected graph must more than the number of nodes - 1"
            )

        self_loop = kwargs.get("self_loop", True)
        repeated_edges = kwargs.get("repeated_edges", True)
        if not repeated_edges:
            max_edge = Graph._calc_max_edge(point_count, False, self_loop)
            if edge_count > max_edge:
                raise Exception(
                    "the number of edges of this kind of graph which has %d vertexes must be less than or equal to %d."
                    % (point_count, max_edge))

        weight_limit = kwargs.get("weight_limit", (1, 1))
        if not list_like(weight_limit):
            weight_limit = (1, weight_limit)
        weight_gen = kwargs.get(
            "weight_gen",
            lambda: random.randint(weight_limit[0], weight_limit[1]))

        used_edges = set()
        graph = Graph.tree(point_count, weight_gen=weight_gen, directed=False)

        for edge in graph.iterate_edges():
            if not repeated_edges:
                used_edges.add((edge.start, edge.end))
                used_edges.add((edge.end, edge.start))

        i = point_count - 1
        while i < edge_count:
            u = random.randint(1, point_count)
            v = random.randint(1, point_count)

            if (not self_loop and u == v) or (not repeated_edges and
                                              (u, v) in used_edges):
                # Then we generate a new pair of nodes
                continue

            graph.add_edge(u, v, weight=weight_gen())

            if not repeated_edges:
                used_edges.add((u, v))
                used_edges.add((v, u))

            i += 1

        return graph

    @staticmethod
    def connected(point_count, edge_count, directed=False, **kwargs):
        """connected(point_count, edge_count, **kwargs) -> Graph
           Factory method. Return a connected graph with point_count vertexes
           int point_count -> the count of vertexes
           bool directed -> whether the graph is directed
        """
        if directed:
            return Graph.DAG(point_count, edge_count, **kwargs)
        else:
            return Graph.UDAG(point_count, edge_count, **kwargs)

    @staticmethod
    def hack_spfa(point_count, **kwargs):
        """hack_spfa(point_count, **kwargs) -> None
           Factory method. Return a spfa graph with point_count vertexes
           int point_count -> the count of vertexes
           **kwargs(Keyword args):
               bool directed = False -> whether the chain is directed(true:directed,false:not directed)
               (int,int) weight_limit = (1,1) -> the limit of weight. index 0 is the min limit, and index 1 is the max limit(both included)
               int weight_limit -> If you use a int for this arg, it means the max limit of the weight(included)
               int extra_edge = 2 -> the number of extra edges
               int/float weight_gen() 
                   = lambda: random.randint(weight_limit[0], weight_limit[1]) 
                   -> the generator of the weights. It should return the weight. The default way is to use the random.randint()
        """
        directed = kwargs.get("directed", False)
        extraedg = kwargs.get("extra_edge", 2)
        weight_limit = kwargs.get("weight_limit", (1, 1))
        if not list_like(weight_limit):
            weight_limit = (1, weight_limit)
        weight_gen = kwargs.get(
            "weight_gen",
            lambda: random.randint(weight_limit[0], weight_limit[1]))

        point_to_skip = point_count + 3
        graph = Graph(point_count, directed)
        if point_count % 2 == 1:
            point_to_skip = point_count / 2 + 1
        half = int(point_count / 2)

        for i in range(1, half):
            (x, y) = (i, i + 1)
            graph.add_edge(x + (x >= point_to_skip),
                           y + (y >= point_to_skip),
                           weight=weight_gen())
            (x, y) = (i + half, i + half + 1)
            graph.add_edge(x + (x >= point_to_skip),
                           y + (y >= point_to_skip),
                           weight=weight_gen())
        for i in range(1, half + 1):
            (x, y) = (i, i + half)
            graph.add_edge(x + (x >= point_to_skip),
                           y + (y >= point_to_skip),
                           weight=weight_gen())

        for i in range(extraedg):
            u = random.randint(1, point_count)
            v = random.randint(1, point_count)
            graph.add_edge(u, v, weight=weight_gen())

        return graph

    @staticmethod
    def _calc_max_edge(point_count, directed, self_loop):
        max_edge = point_count * (point_count - 1)
        if not directed:
            max_edge //= 2
        if self_loop:
            max_edge += point_count
        return max_edge

    @staticmethod
    def forest(point_count, tree_count, **kwargs):
        """
        Return a forest with point_count vertexes and tree_count trees.
        Args:
            point_count: the count of vertexes
            tree_count: the count of trees
        """
        if tree_count <= 0 or tree_count > point_count:
            raise ValueError("tree_count must be between 1 and point_count")
        tree = Graph.tree(point_count, **kwargs)
        tree_edges = list(tree.iterate_edges())
        result = Graph(point_count, tree.directed)
        need_add = random.sample(tree_edges, len(tree_edges) - tree_count + 1)
        for edge in need_add:
            result.add_edge(edge.start, edge.end, weight=edge.weight)
        return result


class GraphMatrix:
    """
    Class GraphMatrix: A class of the graph represented by adjacency matrix.

    *Deprecation warning: This class may be removed after a generic matrix class is implemented in the project.*
    """

    T = TypeVar('T')

    def __init__(self,
                 graph: Graph,
                 default: T = -1,
                 merge: Callable[[T, Edge],
                                 T] = lambda val, edge: edge.weight):
        """
        Args:
            graph: the graph to convert,
            default: the default value when the edge does not exist,
            merge: the mapping from the old values in matrix and the edges to the new values in matrix.
        """
        n = len(graph.edges)
        self.matrix = [[default for _ in range(n)] for _ in range(n)]
        for edge in graph.iterate_edges():
            self.matrix[edge.start][edge.end] = merge(
                self.matrix[edge.start][edge.end], edge)

    def __str__(self):
        return '\n'.join(
            [' '.join(map(str, row[1:])) for row in self.matrix[1:]])

    def __call__(self, u: int, v: int):
        return self.matrix[u][v]

    def __iter__(self):
        return self.matrix.__iter__()
