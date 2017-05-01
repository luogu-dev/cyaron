import random


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


class Graph:
    """Class Graph: A class of the graph
    """
    def __init__(self, point_count):
        """__init__(self, point_count) -> None
            Initialize a graph.
            int point_count -> the count of the vertexes in the graph.
        """
        self.edges = [[] for i in range(point_count+1)]

    def __str__(self):
        """__str__(self) -> str
            Return a string to output the graph. The string contains all the edges of the graph, splits with "\n".
        """
        buf = []
        for edge in self.iterate_edges():
            buf.append(str(edge))

        return "\n".join(buf)

    def iterate_edges(self):
        """iterate_edges(self) -> Edge
            Iter the graph. Order by the start vertex.
        """
        for node in self.edges:
            for edge in node:
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
                bool directed = True -> whether the graph is directed(true:directed,false:not directed)
                                        not directed means if you added the edge x->y, you would also add the edge y->x
        """
        weight = kwargs.get("weight", 1)
        directed = kwargs.get("directed", True)
        self.__add_edge(x, y, weight)
        if not directed:
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
        """
        return Graph.tree(point_count, 0, 1, **kwargs)

    @staticmethod
    def tree(point_count, chain=0, flower=0, **kwargs):
        """tree(point_count, chain=0, flower=0, **kwargs) -> Graph
               Factory method. Return a tree with point_count vertexes.
               int point_count -> the count of vertexes
               bool chain = 0 -> whether the tree is a chain
               bool flower = 0 -> whether the tree is a flower
               NOTICE:only either chain or flower can be True
               **kwargs(Keyword args):
                   bool directed = True -> whether the chain is directed(true:directed,false:not directed)
                   (int,int) weight_limit = (1,1) -> the limit of weight. index 0 is the min limit, and index 1 is the max limit(both included)
                   int weight_limit -> If you use a int for this arg, it means the max limit of the weight(included)
        """
        directed = kwargs.get("directed", True)
        weight_limit = kwargs.get("weight_limit", (1, 1))
        if not isinstance(weight_limit, tuple):
            weight_limit = (1, weight_limit)

        if not 0 <= chain <= 1 or not 0 <= flower <= 1:
            raise Exception("chain and flower must be between 0 and 1")
        if chain+flower > 1:
            raise Exception("chain plus flower must be smaller than 1")

        graph = Graph(point_count)
        chain_count = (point_count-1) * chain
        flower_count = (point_count-1) * flower
        random_count = point_count - 1 - chain_count - flower_count

        for i in range(2, chain_count+2):
            weight = random.randint(weight_limit[0], weight_limit[1])
            graph.add_edge(i-1, i, weight=weight, directed=directed)

        for i in range(chain_count+2, chain_count+flower_count+2):
            weight = random.randint(weight_limit[0], weight_limit[1])
            graph.add_edge(1, i, weight=weight, directed=directed)

        for i in range(point_count-random_count+1, point_count+1):
            weight = random.randint(weight_limit[0], weight_limit[1])
            u = random.randrange(1, i)
            graph.add_edge(u, i, weight=weight, directed=directed)

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
                   bool directed = True -> whether the chain is directed(true:directed,false:not directed)
                   (int,int) weight_limit = (1,1) -> the limit of weight. index 0 is the min limit, and index 1 is the max limit(both included)
                   int weight_limit -> If you use a int for this arg, it means the max limit of the weight(included)
        """
        directed = kwargs.get("directed", True)
        weight_limit = kwargs.get("weight_limit", (1, 1))
        if not isinstance(weight_limit, tuple):
            weight_limit = (1, weight_limit)

        if not 0 <= left <= 1 or not 0 <= right <= 1:
            raise Exception("left and right must be between 0 and 1")
        if left+right > 1:
            raise Exception("left plus right must be smaller than 1")

        can_left = {1}
        can_right = {1}
        graph = Graph(point_count)
        for i in range(2, point_count+1):
            edge_pos = random.uniform(0, 1)
            weight = random.randint(weight_limit[0], weight_limit[1])

            node = 0
            if edge_pos < left or left+right < edge_pos <= (1.0-left-right)/2: # Left
                node = random.choice(tuple(can_left))
                can_left.remove(node)
            elif left <= edge_pos <= left+right or (1.0-left-right)/2 < edge_pos < 1: # Right
                node = random.choice(tuple(can_right))
                can_right.remove(node)

            graph.add_edge(node, i, weight=weight, directed=directed)
            can_left.add(i)
            can_right.add(i)

        return graph

    @staticmethod
    def graph(point_count, edge_count, **kwargs):
        """graph(point_count, edge_count, **kwargs) -> Graph
               Factory method. Return a graph with point_count vertexes and edge_count edges.
               int point_count -> the count of vertexes
               int edge_count -> the count of edges
               **kwargs(Keyword args):
                   bool directed = True -> whether the chain is directed(true:directed,false:not directed)
                   (int,int) weight_limit = (1,1) -> the limit of weight. index 0 is the min limit, and index 1 is the max limit(both included)
                   int weight_limit -> If you use a int for this arg, it means the max limit of the weight(included)
        """
        directed = kwargs.get("directed", True)
        weight_limit = kwargs.get("weight_limit", (1,1))
        if not isinstance(weight_limit, tuple):
            weight_limit = (1, weight_limit)

        graph = Graph(point_count)
        for i in range(edge_count):
            u = random.randint(1, point_count)
            v = random.randint(1, point_count)
            weight = random.randint(weight_limit[0], weight_limit[1])
            graph.add_edge(u, v, weight=weight, directed=directed)

        return graph


