from gerrychain import Graph

from ..benchmark_framework.benchmark import Benchmark


def calculate_maximum_degree(_graph: Graph) -> list[float]:
    return [1]


benchmark = Benchmark("Maximum Degree", 1, calculate_maximum_degree)
