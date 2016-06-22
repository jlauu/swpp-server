class Graph:
    def __init__(self):
        self.nodes = {} # id -> elem
        self.adjlist = {} # id -> [id]
        self.ids = {} # elem -> id
        self.uuid = 1
        self.groups = {} # id -> group
        self._ngroups = 0

    def getNodes(self):
        for i,n in self.nodes.items():
            yield n

    def getID (self, elem):
        return self.ids[elem]

    def addNode(self, n):
        if n not in self.ids:
            self.ids[n] = self.uuid
            self.nodes[self.uuid] = n
            self.groups[self.uuid] = self._ngroups
            self.uuid += 1
            self._ngroups += 1
        return self.ids[n]

    def addEdge(self, src, dest):
        if src not in self.ids.keys():
            self.addNode(src)
            self.adjlist[self.getID(src)] = []
        if dest not in self.ids.keys():
            self.addNode(dest)
            self.adjlist[self.getID(dest)] = []
        edges = self.adjlist[self.getID(src)]
        gs = [self.groups[self.getID(n)] for n in [src,dest]]
        if gs[0] != gs[1]:
            group = min(gs)
            self.groups[src] = group
            self.groups[dest] = group
            self._ngroups -= 1
        node = self.getID(dest)
        if node not in edges:
            edges.append(self.getID(dest))

    def outputEdgeCSV(self, delimiter=","):
        rows = []
        for src, nodes in self.adjlist.items():
            for dest in nodes:
                rows.append("%s,%s" % (src, dest))
        return "\n".join(rows)

    def outputIdCSV(self, delimiter=","):
        return "\n".join(["%s,%s" % (uid,url) for url,uid in self.ids.items()])

