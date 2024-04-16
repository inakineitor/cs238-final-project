from ..benchmark_framework.benchmark import Benchmark


class AverageDegreeBenchmark(Benchmark):
    def score_graph(self, graph) -> float:
        degrees = list(dict(graph.degree).values())
        return sum(degrees) / len(degrees)
