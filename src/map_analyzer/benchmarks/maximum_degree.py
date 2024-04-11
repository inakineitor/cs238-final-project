from gerrychain import Graph

from ..benchmark_framework.benchmark import Benchmark


class MaximumDegreeBenchmark(Benchmark):
    def score_graph(self, graph) -> float:
        return 1
