from gerrychain import Graph
import networkx as nx

from .graph_generating_model import GraphGeneratingModel, GraphGeneration
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
import random
import math


class TriangleEdgeDeletionModel(GraphGeneratingModel):
    p_delete: float

    def __init__(self, p_delete: float, keep_connected: bool, deter: bool):
        """
        Constructor for this model.
        """
        self.p_delete = p_delete
        self.deterministic = deter
        self.keep_connected = keep_connected

    def generate_graph(self, constraints, seed=None) -> GraphGeneration[None]:

        num_points = constraints.num_nodes

        # Create Delaunay Configuration
        rng = np.random.default_rng(seed)
        points = rng.random((num_points, 2))
        tri = Delaunay(points)

        edited_p = {}  # maps vertices to edited (higher) probabilities of edge removals
        edges = []
        edge_htable = set()
        g = nx.Graph(edges)
        for triangle in tri.simplices:
            tups = [0, 0, 0]
            # Get the three edge tuples (a, b), (b, c), (a, c) for the triangle [a, b, c]
            for i in range(1, len(triangle) + 1):
                # FIX: There is a type error here
                tups[i - 1] = (
                    min([triangle[i - 1], triangle[i % (len(triangle) - 1)]]),
                    max([triangle[i - 1], triangle[i % (len(triangle) - 1)]]),
                )

            for t in tups:  # process this triangle
                a, b = t
                if t not in edge_htable:
                    edge_htable.add(t)
                    g.add_edge(a, b)
                    edges.append(t)

        if not self.deterministic:  # probabilistic deletion
            continueflag = False
            for i, e in enumerate(
                g.edges
            ):  # if deleting would cause the graph to become non-connected, then don't delete
                if rng.random() <= self.p_delete or continueflag:
                    u, v = e
                    if self.keep_connected:
                        if not nx.is_connected(
                            g
                        ):  # if this removal makes graph disconnected,
                            g.add_edge(u, v)  # add it back
                            continueflag = True  # and remove again next time
                            # print("Edge restored bc connectivity violation")
                        else:
                            continueflag = False

            # TODO - add post-pruning step here that makes more leaves
            # graph = Graph(nx.Graph(edges))
            return GraphGeneration(graph=g, metadata=None)

        else:  # deterministic sampling
            continueflag = False
            edges = [e for e in g.edges]
            to_remove = random.sample(edges, math.ceil(self.p_delete * len(edges)))
            edges_minus_to_remove = [e for e in edges if e not in to_remove]
            for e in to_remove:
                # if continueflag:
                #     random_edge = random.choice(edges_minus_to_remove)
                #     a, b = random_edge
                #     edges.remove(random_edge)
                #     g.remove_edge(a, b)
                #     if not nx.is_connected(g):  # add it back
                #         g.add_edge(a, b)
                #         edges.append(random_edge)
                #         continueflag = True
                #         print("Edge restored bc connectivity violation")
                #     else:
                #         continueflag = False

                a, b = e
                edges.remove(e)
                g.remove_edge(a, b)
                if self.keep_connected:
                    if not nx.is_connected(g):  # add it back
                        edges.append(e)
                        g.add_edge(a, b)
                        continueflag = True
                        # print("Edge restored bc connectivity violation")
                else:
                    continueflag = False
            return GraphGeneration(graph=g, metadata=None)


## Some Heuristics from lawrence

#     a, b = t  # FIX: There is also a type error here
#     if rng.random() <= max(
#         edited_p.get(a, self.p_delete), edited_p.get(b, self.p_delete)
#     ):
#         edited_p[a] = edited_p.get(a, self.p_delete) + self.p_delete
#         edited_p[b] = edited_p.get(b, self.p_delete) + self.p_delete
#         continue
