from gerrychain import Graph
import networkx as nx

from .graph_generating_model import GraphGeneratingModel


class TriangleDeletionModel(GraphGeneratingModel):
    def generate_graph(self, seed=None) -> Graph:
        graph = nx.Graph()
        graph.add_node(1)
        return Graph.from_networkx(graph)
