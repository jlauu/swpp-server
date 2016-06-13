class Graph:
    def __init__(self):
        self.nodes = []
        self.adjlist = {}
        self.ids = {}
        self.uuid = 1

    def getID (self, elem):
        return self.ids[elem]

    def addNode(self, n):
        if n not in self.nodes:
            self.ids[n] = self.uuid
            self.uuid += 1
            self.nodes.append(n)
        return self.ids[n]

    def addEdge(self, src, dest):
        if src not in self.ids.keys():
            self.addNode(src)
            self.adjlist[self.getID(src)] = []
        if dest not in self.ids.keys():
            self.addNode(dest)
            self.adjlist[self.getID(dest)] = []
        edges = self.adjlist[self.getID(src)]
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

