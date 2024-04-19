from gerrychain import Graph
import networkx as nx
from typing import Callable

from .graph_generating_model import GraphGeneratingModel
import numpy as np


class TriangleEdgeDeletionModel(GraphGeneratingModel):
    distance_metric: Callable[[float, float], float]

    def __init__(self, distance_metric=np.linalg.norm):
        """
        Constructor for this model.
        """
        self.distance_metric = distance_metric

    def generate_graph(self, seed=None, param_dict=None) -> Graph:
        # dist = lambda x, y: sum(abs(a - b) for a, b in zip(x, y)) # Use this
        graph = nx.waxman_graph(10, 0.5, 0.1, metric=self.distance_metric)
        return graph
