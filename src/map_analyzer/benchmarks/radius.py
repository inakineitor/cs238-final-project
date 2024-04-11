from gerrychain import Graph

from ..benchmark_framework.benchmark import Benchmark


def calculate_radius(_graph: Graph) -> list[float]:
    return [1]


benchmark = Benchmark("Radius", 1, calculate_radius)
