from gerrychain import Graph

from ..benchmark_framework.benchmark import Benchmark


class RadiusBenchmark(Benchmark):
    def score_graph(self, graph) -> float:
        return 1
