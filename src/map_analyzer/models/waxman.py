from gerrychain import Graph
import networkx as nx
from typing import Callable

from .graph_generating_model import GraphGeneratingModel
import numpy as np


class WaxmanModel(GraphGeneratingModel):
    distance_metric: Callable[[float, float], float]

    def __init__(self, distance_metric=np.linalg.norm):
        """
        Constructor for this model.

        :distance_metric: function used to calculate the distance between two nodes in the graph for use in the Waxman model
        """
        self.distance_metric = distance_metric

    def generate_graph(self, seed=None, param_dict=None) -> Graph:
        num_points = param_dict["n"]  # TODO: Add typing to `param_dict`
        graph = nx.waxman_graph(num_points, 0.5, 0.1, metric=self.distance_metric)
        return graph
