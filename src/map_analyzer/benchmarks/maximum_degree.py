from ..benchmark_framework.benchmark import Benchmark


class MaximumDegreeBenchmark(Benchmark):
    def score_graph(self, graph) -> float:
        return max(list(dict(graph.degree).values()))
