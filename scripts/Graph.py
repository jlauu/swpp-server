class Graph:
    def __init__(self):
        self.nodes = {} # id -> elem
        self.adjlist = {} # id -> [id]
        self._undirectedEdges = {} # id -> [id]
        self.ids = {} # elem -> id
        self.groups = {} # id -> group id
        self.uuid = 1

    def getNodes(self):
        for i,n in self.nodes.items():
            yield n

    def addNode(self, n):
        if n not in self.ids:
            self.ids[n] = self.uuid
            self.nodes[self.uuid] = n
            self.groups[self.uuid] = None
            self.uuid += 1
        return self.ids[n]

    def getConnectedComponents(self):
        i = 0
        components = {}
        for v in self.nodes:
            if self.groups[v] is None:
                components[i] = self._dfs(v)
                for u in components[i]:
                    self.groups[u] = i
                i += 1
        return components

    def _dfs(self, start):
        visited, stack = set(), [start]
        while stack:
            v = stack.pop()
            if v not in visited:
                visited.add(v)
                stack.extend(set(self.adjlist[v]) - visited)
                stack.extend(set(self._undirectedEdges[v]) - visited)
        return list(visited)

    def addEdge(self, src, dest):
        if src not in self.ids.keys():
            self.addNode(src)
            self.adjlist[self.ids[src]] = []
            self._undirectedEdges[self.ids[src]] = []
        if dest not in self.ids.keys():
            self.addNode(dest)
            self.adjlist[self.ids[dest]] = []
            self._undirectedEdges[self.ids[dest]] = []
        edges = self.adjlist[self.ids[src]]
        u_edges = self._undirectedEdges[self.ids[dest]]
        s_id = self.ids[src]
        d_id = self.ids[dest]
        if d_id not in edges:
            edges.append(d_id)
        if s_id not in u_edges:
            u_edges.append(s_id)


    def outputEdgeCSV(self, delimiter=","):
        rows = []
        for src, nodes in self.adjlist.items():
            for dest in nodes:
                rows.append("%s,%s" % (src, dest))
        return "\n".join(rows)

    def outputIdCSV(self, delimiter=","):
        return "\n".join(["%s,%s" % (uid,url) for url,uid in self.ids.items()])

