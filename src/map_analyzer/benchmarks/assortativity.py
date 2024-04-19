import networkx as nx

from ..benchmark_framework.benchmark import Benchmark


class AssortativityBenchmark(Benchmark):
    def score_graph(self, graph) -> float:
        return nx.degree_assortativity_coefficient(graph)
