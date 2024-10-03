import unittest
from cyaron import Graph


class UnionFindSet:
    def __init__(self, size):
        self.father = [0] + [i + 1 for i in range(size)]

    def get_father(self, node):
        if self.father[node] == node:
            return node
        else:
            self.father[node] = self.get_father(self.father[node])
            return self.father[node]

    def merge(self, l, r):
        l = self.get_father(l)
        r = self.get_father(r)
        self.father[l] = r

    def test_same(self, l, r):
        return self.get_father(l) == self.get_father(r)


def tarjan(graph, n):
    def new_array(len, val=0):
        return [val for _ in range(len+1)]

    instack = new_array(n, False)
    low = new_array(n)
    dfn = new_array(n, 0)
    stap = new_array(n)
    belong = new_array(n)
    var = [0, 0, 0] # cnt, bc, stop
    # cnt = bc = stop = 0

    def dfs(cur):
        var[0] += 1
        dfn[cur] = low[cur] = var[0]
        instack[cur] = True
        stap[var[2]] = cur
        var[2] += 1

        for v in graph.edges[cur]:
            if dfn[v.end] == 0:
                dfs(v.end)
                low[cur] = min(low[cur], low[v.end])
            elif instack[v.end]:
                low[cur] = min(low[cur], dfn[v.end])

        if dfn[cur] == low[cur]:
            v = cur + 1 # set v != cur
            var[1] += 1
            while v != cur:
                var[2] -= 1
                v = stap[var[2]]
                instack[v] = False
                belong[v] = var[1]

    for i in range(n):
        if dfn[i+1] == 0:
            dfs(i+1)

    return belong


class TestGraph(unittest.TestCase):

    def test_self_loop(self):
        graph_size = 20
        for _ in range(20):
            graph = Graph.graph(graph_size, int(graph_size*2), self_loop=True)
            has_self_loop = max([e.start == e.end for e in graph.iterate_edges()])
            if has_self_loop:
                break
        self.assertTrue(has_self_loop)

        for _ in range(10):
            graph = Graph.graph(graph_size, int(graph_size*2), self_loop=False)
            self.assertFalse(max([e.start == e.end for e in graph.iterate_edges()]))

    def test_repeated_edges(self):
        graph_size = 20
        for _ in range(20):
            graph = Graph.graph(graph_size, int(graph_size*2), repeated_edges=True)
            edges = [(e.start, e.end) for e in graph.iterate_edges()]
            has_repeated_edges = len(edges) > len(set(edges))
            if has_repeated_edges:
                break
        self.assertTrue(has_repeated_edges)

        for _ in range(10):
            graph = Graph.graph(graph_size, int(graph_size*2), repeated_edges=False)
            edges = list(graph.iterate_edges())
            self.assertEqual(len(edges), len(set(edges)))

    def test_tree_connected(self):
        graph_size = 20
        for _ in range(20):
            ufs = UnionFindSet(graph_size)
            tree = Graph.tree(graph_size)
            for edge in tree.iterate_edges():
                ufs.merge(edge.start, edge.end)
            for i in range(graph_size-1):
                self.assertTrue(ufs.test_same(i+1, i+2))
            

    def test_DAG(self):
        graph_size = 20
        for _ in range(10): # test 10 times
            ufs = UnionFindSet(graph_size)
            graph = Graph.DAG(graph_size, int(graph_size*1.6), repeated_edges=False, self_loop=False, loop=True)

            self.assertEqual(len(list(graph.iterate_edges())), int(graph_size*1.6))

            for edge in graph.iterate_edges():
                ufs.merge(edge.start, edge.end)
            for i in range(graph_size-1):
                self.assertTrue(ufs.test_same(i+1, i+2))

    def test_DAG_without_loop(self):
        graph_size = 20
        for _ in range(10): # test 10 times
            ufs = UnionFindSet(graph_size)
            graph = Graph.DAG(graph_size, int(graph_size*1.6), repeated_edges=False, self_loop=False, loop=False)

            self.assertEqual(len(list(graph.iterate_edges())), int(graph_size*1.6))

            for edge in graph.iterate_edges():
                ufs.merge(edge.start, edge.end)
            for i in range(graph_size-1):
                self.assertTrue(ufs.test_same(i+1, i+2))

            belong = tarjan(graph, graph_size)
            self.assertEqual(max(belong), graph_size)

    def test_undirected_graph(self):
        graph_size = 20
        for _ in range(10): # test 10 times
            ufs = UnionFindSet(graph_size)
            graph = Graph.UDAG(graph_size, int(graph_size*1.6), repeated_edges=False, self_loop=False)

            self.assertEqual(len(list(graph.iterate_edges())), int(graph_size*1.6))

            for edge in graph.iterate_edges():
                ufs.merge(edge.start, edge.end)
            for i in range(graph_size-1):
                self.assertTrue(ufs.test_same(i+1, i+2))

    def test_DAG_boundary(self):
        with self.assertRaises(Exception, msg="the number of edges of connected graph must more than the number of nodes - 1"):
            Graph.DAG(8, 6)
        Graph.DAG(8, 7)

    def test_GraphMatrix(self):
        g = Graph(3, True)
        edge_set = [(2, 3, 3), (3, 3, 1), (2, 3, 7), (2, 3, 4), (3, 2, 1), (1, 3, 3)]
        for u, v, w in edge_set:
            g.add_edge(u, v, weight=w)
        self.assertEqual(str(g.to_matrix()), "-1 -1 3\n-1 -1 4\n-1 1 1")
        self.assertEqual(str(g.to_matrix(default=0)), "0 0 3\n0 0 4\n0 1 1")
        # lambda val, edge: edge.weight
        gcd = lambda a, b: (gcd(b, a % b) if b else a)
        lcm = lambda a, b: a * b // gcd(a, b)
        merge1 = lambda v, e: v if v != -1 else e.weight
        merge2 = lambda val, edge: max(edge.weight, val)
        merge3 = lambda val, edge: min(edge.weight, val)
        merge4 = lambda val, edge: gcd(val, edge.weight)
        merge5 = lambda val, edge: lcm(val, edge.weight) if val else edge.weight
        self.assertEqual(str(g.to_matrix(merge=merge1)), "-1 -1 3\n-1 -1 3\n-1 1 1")
        self.assertEqual(str(g.to_matrix(merge=merge2)), "-1 -1 3\n-1 -1 7\n-1 1 1")
        self.assertEqual(str(g.to_matrix(default=9, merge=merge3)), "9 9 3\n9 9 3\n9 1 1")
        self.assertEqual(str(g.to_matrix(default=0, merge=merge4)), "0 0 3\n0 0 1\n0 1 1")
        self.assertEqual(str(g.to_matrix(default=0, merge=merge5)), "0 0 3\n0 0 84\n0 1 1")
