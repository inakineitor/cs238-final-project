import networkx as nx

from ..benchmark_framework.benchmark import Benchmark


class DiameterBenchmark(Benchmark):
    def score_graph(self, graph) -> float:
       # Note: diameter isn't defined for disconnected graphs
       return nx.diameter(graph) if nx.is_connected(graph) else -1
