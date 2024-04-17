from gerrychain import Graph
import networkx as nx

from .graph_generating_model import GraphGeneratingModel
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay


class TriangleEdgeDeletionModel(GraphGeneratingModel):
    def __init__(self, probability: float, num_pts: int):
        """
        Constructor for this model.

        Args:
            probability (float): prob of deleting A SINGLE EDGE from Delaunay tesselation. 
        """
        self.p_delete = probability
        self.n = num_pts


    def generate_graph(self, seed=None) -> Graph:
        # Create Delaunay Configuration
        rng = np.random.default_rng(seed)
        points = rng.random((self.n, 2))
        tri = Delaunay(points)
        
        edited_p = {} # maps vertices to edited (higher) probabilities of edge removals
        edges = []
        edge_htable = set()
        for triangle in tri.simplices:
            tups = [0, 0, 0]
            # Get the three edge tuples (a, b), (b, c), (a, c) for the triangle [a, b, c]
            for i in range(1, len(triangle)+1):
                tups[i-1] = (min([triangle[i-1], triangle[i % (len(triangle) - 1)]]), max([triangle[i-1], triangle[i % (len(triangle)-1)]]))
                
            for t in tups:
                a, b = t
                if rng.random() <= max(edited_p.get(a, self.p_delete), edited_p.get(b, self.p_delete)):
                    edited_p[a] = edited_p.get(a, self.p_delete) + self.p_delete
                    edited_p[b] = edited_p.get(b, self.p_delete) + self.p_delete
                    continue
                if t not in edge_htable:
                    edge_htable.add(t)
                    edges.append(t)
        
        graph = nx.Graph(edges)

        # Return graph 
        return graph

