from scripts.Graph import *
import os, json

def main(filename):
    DATA_DIR = os.path.dirname(filename) + '/'
    graphs = parseGraphCSV(filename)
    for gid, g in graphs.items():
        g_json = formatJSON(gid, g)
        with open(DATA_DIR + "%s.json" % gid, 'w') as f:
            f.write(json.dumps(g_json))

def parseGraphCSV(filename):
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
if __name__ == "__main__":
    import sys
    main(sys.argv[1])
