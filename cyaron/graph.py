import random


class Edge:
    def __init__(self, u, v, w):
        self.start = u
        self.end = v
        self.weight = w

    def __str__(self):
        return "%d %d %d" % (self.start, self.end, self.weight)


class Graph:
    def __init__(self, point_count):
        self.edges = [[] for i in range(point_count+1)]

    def __str__(self):
        buf = []
        for edge in self.iterate_edges():
            buf.append(str(edge))

        return "\n".join(buf)

    def iterate_edges(self):
        for node in self.edges:
            for edge in node:
                yield edge

    def __add_edge(self, x, y, w):
        self.edges[x].append(Edge(x, y, w))

    def add_edge(self, x, y, **kwargs):
        weight = kwargs.get("weight", 1)
        directed = kwargs.get("directed", True)
        self.__add_edge(x, y, weight)
        if not directed:
            self.__add_edge(y, x, weight)

    @staticmethod
    def chain(point_count, **kwargs):
        return Graph.tree(point_count, 1, 0, **kwargs)

    @staticmethod
    def flower(point_count, **kwargs):
        return Graph.tree(point_count, 0, 1, **kwargs)

    @staticmethod
    def tree(point_count, chain=0, flower=0, **kwargs):
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


