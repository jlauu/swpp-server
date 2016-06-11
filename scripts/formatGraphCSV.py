def main(filename):
    graphs = {}
    with open(filename) as f: 
        for line in f:
            parts = line.split(",")
            if parts[0] not in graphs.keys():
                graphs[parts[0]] = Graph()
            g = graphs[parts[0]]
            g.addEdge(parts[2], parts[3])
    for gid, g in graphs.items():
        outputGraphFiles(gid, g)


def outputGraphFiles(gid, graph):
    edges = insertAtStart(graph.outputEdgeCSV(), "%s," % gid)
    urlIds = insertAtStart(graph.outputIdCSV(), "%s," % gid)
    with open("%s-edges.csv" % gid, 'w') as f:
        f.write(edges)
    with open("%s-ids.csv" % gid, 'w') as f:
        f.write(urlIds)

def insertAtStart(lines, text):
    return "\n".join([text + line for line in lines.split("\n")])

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

if __name__ == "__main__":
    import sys
    main(sys.argv[1])
