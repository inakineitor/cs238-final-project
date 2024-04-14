import networkx as nx

from ..benchmark_framework.benchmark import Benchmark


class RadiusBenchmark(Benchmark):
    def score_graph(self, graph) -> float:
       # Note: radius isn't defined for disconnected graphs
       return nx.radius(graph) if nx.is_connected(graph) else -1
