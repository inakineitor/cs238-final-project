from dataclasses import dataclass

from gerrychain import Graph

from map_analyzer.models.graph_generating_model import GraphGeneratingModel
from .benchmark import Benchmark, BenchmarkResults


@dataclass
class BenchmarkOrchestratorResults:
    benchmarks: list[BenchmarkResults]


class BenchmarkOrchestrator:
    benchmarks: list[Benchmark]

    def __init__(self, benchmarks: list[Benchmark]):
        self.benchmarks = benchmarks

    def benchmark_graphs(self, graphs: list[Graph]) -> BenchmarkOrchestratorResults:
        benchmark_outputs = [
            benchmark.benchmark_graphs(graphs) for benchmark in self.benchmarks
        ]
        return BenchmarkOrchestratorResults(benchmarks=benchmark_outputs)

    def benchmark_model(
        self, model: GraphGeneratingModel, num_iters: int, seed: int, extra_params=None
    ) -> BenchmarkOrchestratorResults:
        graphs = model.generate_graphs(num_iters, seed, opt_params=extra_params)
        num_vertices = [g.number_of_nodes() for g in graphs]
        return num_vertices, self.benchmark_graphs(graphs)

    # def benchmark_models(
    #     self, models: list[GraphGeneratingModel], num_iters: int, seed: int
    # ) -> list[BenchmarkOrchestratorResults]:
    #     return [self.benchmark_model(model, num_iters, seed) for model in models]
