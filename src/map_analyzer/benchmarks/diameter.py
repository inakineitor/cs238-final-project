import networkx as nx

from ..benchmark_framework.benchmark import Benchmark


class DiameterBenchmark(Benchmark):
    def score_graph(self, graph) -> float:
       # return 1
       return nx.diameter(graph) # NOTE - This won't work for non-connected graphs
