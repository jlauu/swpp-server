from Graph import *
import os

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
            g.addEdge(parts[1], parts[2])
    for gid, g in graphs.items():
        outputGraphFiles(gid, g)
    return graphs


def outputGraphFiles(gid, graph):
    edges = insertAtStart(graph.outputEdgeCSV(), "%s," % gid)
    urlIds = insertAtStart(graph.outputIdCSV(), "%s," % gid)
    if not os.path.exists(DATADIR):
        os.makedirts(DATADIR)
    with open(DATADIR + "%s-edges.csv" % gid, 'w') as f:
        f.write(edges)
    with open(DATADIR + "%s-ids.csv" % gid, 'w') as f:
        f.write(urlIds)

def insertAtStart(lines, text):
    return "\n".join([text + line for line in lines.split("\n")])

if __name__ == "__main__":
    import sys
    main(sys.argv[1])
