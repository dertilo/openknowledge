from util import data_io
import networkx as nx
from matplotlib import pyplot as plt

if __name__ == '__main__':
    graph = nx.DiGraph()
    data = [d['a'] for d in data_io.read_jsonl('datasample.json')]

    nodes = [node for d in data for node in d['nodes']]
    for n in nodes:
        graph.add_node(n['id'],**n)

    for n in [r for d in data for r in d['rels']]:
        graph.add_edge(n['start']['id'],n['end']['id'],**n)

    plt.figure(figsize=(50, 50))
    pos = nx.drawing.layout.spring_layout(graph)
    labels = {d['id']:d['properties']['EntityName'] for d in nodes}
    nx.draw_networkx(graph,pos=pos,labels=labels,font_size=9)
    plt.savefig("graph.png")
    plt.show()

    print()