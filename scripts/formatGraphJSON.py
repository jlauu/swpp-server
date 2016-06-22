from Graph import *
import os, json

DATADIR = '../data/'

def main(filename):
    graphs = {}
    with open(DATADIR + filename) as f: 
        for line in f:
            parts = line.split(",")
            if parts[0] not in graphs.keys():
                graphs[parts[0]] = Graph()
            g = graphs[parts[0]]
            if 'http' not in parts[2]:
                parts[2] = parts[1] + parts[2]
            g.addEdge(parts[1].strip(), parts[2].strip())
    for gid, g in graphs.items():
        outputGraphFiles(gid, g)
    return graphs


def outputGraphFiles(gid, graph):
    nodes = []
    links = []
    for url, index in graph.ids.items():
        nodes.append({'url':url, 'id': index})
    for src, dests in graph.adjlist.items():
        for dest in dests:
            if dest:
                links.append({'source':src, 'target': dest})
    if not os.path.exists(DATADIR):
        os.makedirs(DATADIR)
    links = [ {'value':1,'source': l['source'], 'target':l['target']} for l in links]
    print(len(links))
    with open("%s.json" % gid, 'w') as f:
        f.write(json.dumps({'nodes':nodes,'links':links}))

if __name__ == "__main__":
    import sys
    main(sys.argv[1])
