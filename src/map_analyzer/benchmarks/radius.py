import networkx as nx

from ..benchmark_framework.benchmark import Benchmark


class RadiusBenchmark(Benchmark):
    def score_graph(self, graph) -> float:
        return nx.radius(graph)
