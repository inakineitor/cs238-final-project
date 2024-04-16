import networkx as nx

from ..benchmark_framework.benchmark import Benchmark


class ClusteringCoefficientBenchmark(Benchmark):
    def score_graph(self, graph) -> float:
       return nx.transitivity(graph)
