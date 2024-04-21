from gerrychain import Graph
import networkx as nx

from .graph_generating_model import GraphGeneratingModel, GraphGeneration
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay


class TriangleEdgeDeletionModel(GraphGeneratingModel):
    p_delete: float

    def __init__(self, p_delete: float):
        """
        Constructor for this model.
        """
        self.p_delete = p_delete

    def generate_graph(self, constraints, seed=None) -> GraphGeneration[None]:

        num_points = constraints.num_nodes

        # Create Delaunay Configuration
        rng = np.random.default_rng(seed)
        points = rng.random((num_points, 2))
        tri = Delaunay(points)

        edited_p = {}  # maps vertices to edited (higher) probabilities of edge removals
        edges = []
        edge_htable = set()
        for triangle in tri.simplices:
            tups = [0, 0, 0]
            # Get the three edge tuples (a, b), (b, c), (a, c) for the triangle [a, b, c]
            for i in range(1, len(triangle) + 1):
                # FIX: There is a type error here
                tups[i - 1] = (
                    min([triangle[i - 1], triangle[i % (len(triangle) - 1)]]),
                    max([triangle[i - 1], triangle[i % (len(triangle) - 1)]]),
                )

            for t in tups:
                a, b = t  # FIX: There is also a type error here
                if rng.random() <= max(
                    edited_p.get(a, self.p_delete), edited_p.get(b, self.p_delete)
                ):
                    edited_p[a] = edited_p.get(a, self.p_delete) + self.p_delete
                    edited_p[b] = edited_p.get(b, self.p_delete) + self.p_delete
                    continue
                if t not in edge_htable:
                    edge_htable.add(t)
                    edges.append(t)

        graph = Graph(nx.Graph(edges))

        # TODO - add post-pruning step here that makes more leaves

        # Return graph
        return GraphGeneration(graph=graph, metadata=None)
