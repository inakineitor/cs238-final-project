from dataclasses import dataclass

import numpy as np
from gerrychain import Graph

from map_analyzer.models.graph_generating_model import GraphGeneratingModel
from .benchmark import Benchmark


@dataclass
class BenchmarkResults:
    minimum: float
    mean: float
    maximum: float
    all_vals: list[float]


@dataclass
class BenchmarkOrchestratorResults:
    benchmarks: list[BenchmarkResults]


def run_single_benchmark(benchmark: Benchmark, graphs: list[Graph]) -> BenchmarkResults:
    scores = benchmark.score_graphs(graphs)
    return BenchmarkResults(
        minimum=np.min(scores),
        mean=float(np.mean(scores)),
        maximum=np.max(scores),
        all_vals=scores,
    )


class BenchmarkOrchestrator:
    benchmarks: list[Benchmark]

    def __init__(self, benchmarks: list[Benchmark]):
        self.benchmarks = benchmarks

    def benchmark_model(
        self, model: GraphGeneratingModel, num_iters: int, seed: int
    ) -> BenchmarkOrchestratorResults:
        graphs = model.generate_graphs(num_iters, seed)
        benchmark_outputs = [
            run_single_benchmark(benchmark, graphs) for benchmark in self.benchmarks
        ]
        return BenchmarkOrchestratorResults(benchmarks=benchmark_outputs)

    def benchmark_models(
        self, models: list[GraphGeneratingModel], num_iters: int, seed: int
    ) -> list[BenchmarkOrchestratorResults]:
        return [self.benchmark_model(model, num_iters, seed) for model in models]
