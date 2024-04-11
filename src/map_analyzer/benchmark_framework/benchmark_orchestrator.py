from gerrychain import Graph

from map_analyzer.models.graph_generating_model import GraphGeneratingModel
from .benchmark import Benchmark


class BenchmarkResults:
    benchmarks: dict[str, BenchmarkResult]


class BenchmarkOrchestrator:
    benchmarks: list[Benchmark]

    def __init__(self, benchmarks: list[Benchmark]):
        self.benchmarks = benchmarks

    def run_model_benchmark(self, model: GraphGeneratingModel):
        pass

    def benchmark_modles(
        self, graphs: list[GraphGeneratingModel]
    ) -> list[tuple[str, BenchmarkResults]]:
        pass
