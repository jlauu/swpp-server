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
    

def formatJSON(gid, graph, clusters={}):
    """Given a graph, groups nodes according to connected components and returns
       a json for the d3 front-end to use"""
    nodes = []
    links = []
    components = graph.getConnectedComponents(clusters)
    for n_id in graph.nodes:
        nodes.append({'url':graph.nodes[n_id], 'id': n_id, 'group':graph.groups[n_id]})
    for src, dests in graph.adjlist.items():
        for dest in dests:
            if dest:
                links.append({'source':src, 'target': dest})
    links = [ {'value':1,'source': l['source'], 'target':l['target']} for l in links]
    return {
            'user_id': gid,
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

    def getConnectedComponents(self, init={}):
        """Returns a list of connected components in the graph.
           Pass init as a map of node ids to initial group ids"""
        i = 0
        self.visited = set()
        components = {}
        for gid in init.values():
            components[gid] = []
        for v in self.nodes:
            while i in components:
                i += 1
            if v not in self.visited:
                components[i] = self._dfs(v, self.visited)
                for u in components[i]:
                    if u in init:
                        [self.groups.update({w:init[u]}) for w in components[i]]
                        components[init[u]].extend(components[i])
                        del components[i]
                        break
                    else:
                        self.groups[u] = i
        cs = {}
        for k,c in components.items():
            if c:
                cs[k] = c
        return cs

    def _dfs(self, start, visited=set()):
        component, stack = set(), [start]
        while stack:
            print('\tVisited:', visited)
            print('\tStack:', stack)
            v = stack.pop()
            if v not in visited:
                visited.add(v)
                component.add(v)
                stack.extend(set(self.adjlist[v]) - visited)
                stack.extend(set(self._undirectedEdges[v]) - visited)
        return list(component)

    def outputEdgeCSV(self, delimiter=","):
        rows = []
        for src, nodes in self.adjlist.items():
            for dest in nodes:
                rows.append("%s,%s" % (src, dest))
        return "\n".join(rows)

    def outputIdCSV(self, delimiter=","):
        return "\n".join(["%s,%s" % (uid,url) for url,uid in self.ids.items()])

