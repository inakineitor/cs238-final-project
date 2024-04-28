from dataclasses import dataclass

from gerrychain import Graph

from map_analyzer.benchmark_framework.model_constraint_generator import (
    ModelConstraints,
    generate_constraints_from_graph,
)
from map_analyzer.models.graph_generating_model import (
    GraphGeneratingModel,
    GraphGeneration,
)
from map_analyzer.models.real_life_maps import RealLifeMapMetadata, RealLifeMaps
from .benchmark_rhea import Benchmark, BenchmarkResults


@dataclass
class BenchmarkOrchestratorResults:
    real_map_generation: GraphGeneration[RealLifeMapMetadata]
    real_map_benchmarks: list[BenchmarkResults]
    model_benchmarks: list[list[BenchmarkResults]]


class BenchmarkOrchestrator:
    benchmarks: list[Benchmark]

    def __init__(self, benchmarks: list[Benchmark]):
        self.benchmarks = benchmarks

    def benchmark_graphs(self, graphs: list[Graph]) -> list[BenchmarkResults]:
        benchmark_outputs = [
            benchmark.benchmark_graphs(graphs) for benchmark in self.benchmarks
        ]
        return benchmark_outputs

    def benchmark_model(
        self,
        model: GraphGeneratingModel,
        num_iters: int,
        constraints: ModelConstraints,
        seed: int,
    ) -> list[BenchmarkResults]:
        graph_generations = model.generate_graphs(num_iters, constraints, seed)
        graphs = [graph_generation.graph for graph_generation in graph_generations]
        return self.benchmark_graphs(graphs)

    def benchmark_null_models_against_real(
        self,
        real_life_model: RealLifeMaps,
        models: list[GraphGeneratingModel],
        num_iters: int,
        seed: int,
    ) -> list[BenchmarkOrchestratorResults]:
        control_maps = real_life_model.get_all_graphs()
        all_constraints = [
            generate_constraints_from_graph(graph_generation.graph)
            for graph_generation in control_maps
        ]
        benchmark_outputs = [
            BenchmarkOrchestratorResults(
                real_map_generation=control_map,
                real_map_benchmarks=self.benchmark_graphs([control_map.graph]),
                model_benchmarks=[
                    self.benchmark_model(
                        model=model,
                        num_iters=num_iters,
                        constraints=constraints,
                        seed=seed,
                    )
                    for model in models
                ],
            )
            for control_map, constraints in zip(control_maps, all_constraints)
        ]
        return benchmark_outputs
