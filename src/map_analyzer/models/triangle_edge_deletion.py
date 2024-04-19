from gerrychain import Graph
import networkx as nx

from .graph_generating_model import GraphGeneratingModel
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay


class TriangleEdgeDeletionModel(GraphGeneratingModel):
    def __init__(self, name="TriangleDeletion"):
        """
        Constructor for this model.

        Args:
            probability (float): prob of deleting A SINGLE EDGE from Delaunay tesselation.
        """
        self.name = name

    def generate_graph(self, seed=None, param_dict=None) -> Graph:

        num_points = param_dict["n"]
        p_delete = param_dict["p_delete"]

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
                tups[i - 1] = (
                    min([triangle[i - 1], triangle[i % (len(triangle) - 1)]]),
                    max([triangle[i - 1], triangle[i % (len(triangle) - 1)]]),
                )

            for t in tups:
                a, b = t
                if rng.random() <= max(
                    edited_p.get(a, p_delete), edited_p.get(b, p_delete)
                ):
                    edited_p[a] = edited_p.get(a, p_delete) + p_delete
                    edited_p[b] = edited_p.get(b, p_delete) + p_delete
                    continue
                if t not in edge_htable:
                    edge_htable.add(t)
                    edges.append(t)

        graph = nx.Graph(edges)

        # TODO - add post-pruning step here that makes more leaves

        # Return graph
        return graph
