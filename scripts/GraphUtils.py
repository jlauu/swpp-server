import os, json

def parseGraphCSV(filename):
    """Parses the internal csv of edges and returns a dictionary of graphs"""
    graphs = {}
    with open(filename) as f: 
        for line in f:
            parts = line.split(",")
            if parts[0] not in graphs.keys():
                graphs[parts[0]] = Graph()
            g = graphs[parts[0]]
            if 'http' not in parts[2]:
                parts[2] = parts[1] + parts[2]
            g.addEdge(parts[1].strip(), parts[2].strip())
    return graphs
    

def formatJSON(gid, graph):
    """Given a graph, groups nodes according to connected components and returns
       a json for the d3 front-end to use"""
    nodes = []
    links = []
    components = graph.getConnectedComponents()
    for n_id in graph.nodes:
        nodes.append({'url':graph.nodes[n_id], 'id': n_id, 'group':graph.groups[n_id]})
    for src, dests in graph.adjlist.items():
        for dest in dests:
            if dest:
                links.append({'source':src, 'target': dest})
    links = [ {'value':1,'source': l['source'], 'target':l['target']} for l in links]
    return {
            'nodes':nodes,
            'links':links, 
            'groups': [gid for gid, ns in components.items()]
           }

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

