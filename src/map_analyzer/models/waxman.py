from gerrychain import Graph
import networkx as nx
from typing import Callable

from .graph_generating_model import GraphGeneratingModel, GraphGeneration
import numpy as np


class WaxmanModel(GraphGeneratingModel):
    beta: float
    alpha: float
    distance_metric: Callable[[float, float], float]

    def __init__(self, beta: float, alpha: float, distance_metric=np.linalg.norm):
        """
        Constructor for this model.

        :distance_metric: function used to calculate the distance between two nodes in the graph for use in the Waxman model
        """
        self.beta = beta
        self.alpha = alpha
        self.distance_metric = distance_metric

    def generate_graph(self, constraints, seed=None) -> GraphGeneration[None]:
        num_points = constraints.num_nodes
        # graph = nx.waxman_graph(num_points, self.beta, self.alpha, metric=self.distance_metric)
        # TODO: Add support for distance_metric
        graph = Graph(nx.waxman_graph(num_points, self.beta, self.alpha))
        return GraphGeneration(graph=graph, metadata=None)
