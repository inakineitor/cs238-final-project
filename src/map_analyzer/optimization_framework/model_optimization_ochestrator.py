from dataclasses import dataclass
from typing import Callable, Optional, Union

from numpy import mean
from numpy.random import Generator
from scipy.stats import entropy
from rich.progress import track

from map_analyzer.benchmark_framework.benchmark import BenchmarkResults
from map_analyzer.benchmark_framework.benchmark_orchestrator import (
    BenchmarkOrchestrator,
)
from map_analyzer.benchmark_framework.model_constraint_generator import (
    ModelConstraints,
    generate_constraints_from_graph,
)
from map_analyzer.models.graph_generating_model import GraphGeneratingModel
from map_analyzer.models.real_life_maps import RealLifeMaps
from map_analyzer.optimization_framework.model_parameter_optimizer import (
    AllOptimizationResult,
    ModelParameterOptimizer,
    ParameterBounds,
)

ModelConstructor = Callable[..., GraphGeneratingModel]


@dataclass
class OptimizableModel:
    name: str
    model_constructor: ModelConstructor
    parameter_bounds: ParameterBounds


def calculate_kl_divergence():
    pass


# @dataclass
# class OptimizationResult:
#     benchmarks: list[BenchmarkOptimizationResult]


@dataclass
class ModelOptimizationResult:
    benchmark_focus_results: list[AllOptimizationResult]


class ModelOptimizationOrchestrator:
    optimizers: list[ModelParameterOptimizer]
    benchmark_orchestrator: BenchmarkOrchestrator

    def __init__(
        self,
        optimizers: list[ModelParameterOptimizer],
        benchmark_orchestrator: BenchmarkOrchestrator,
    ):
        self.optimizers = optimizers
        self.benchmark_orchestrator = benchmark_orchestrator

    # TODO: Unfinished implementation of the use of muliple optimizers
    # def optimize_model_against_benchmark(
    #     self,
    #     model_constructor: ModelConstructor,
    #     parameter_bounds: ParameterBounds,
    #     benchmark_focus_index: int,
    # ) -> BenchmarkOptimizationResult:
    #     best_parameters = [0] * len(parameter_bounds)
    #     best_loss = float("inf")
    #     best_loss_vector = [float("inf")] * len(self.benchmark_orchestrator.benchmarks)
    #     # for optimizer in self.optimizers:
    #     #     result = optimizer.find_best_parameters(model_constructor, parameter_bounds, lambda benchmark_results: )
    #     # self.benchmark_orchestrator
    #     pass

    def calculate_kl_divergence_loss(
        self,
        real_benchmarks: list[BenchmarkResults],
        model_benchmarks: list[BenchmarkResults],
    ) -> list[float]:
        # return a list of KL divergence values between the real and model benchmarks
        # for each benchmark
        # TODO: Check if this is the correct way to calculate KL divergence
        return [
            # entropy(real_benchmarks[i].all_vals, model_benchmarks[i].all_vals)
            mean(model_benchmarks[i].all_vals)
            for i in range(len(real_benchmarks))
        ]

    # def _optimize_model_single_optimizer() -> ModelOptimizationResult:

    def optimize_null_model_against_real(
        self,
        real_constraints: list[ModelConstraints],
        real_benchmarks: list[BenchmarkResults],
        optimizable_model: OptimizableModel,
        seed: Optional[Union[int, Generator]] = None,
    ) -> ModelOptimizationResult:
        def all_loss_function(*model_parameters):
            model = optimizable_model.model_constructor(*model_parameters)
            graph_generations = [
                model.generate_graph(constraints=real_constraint, seed=seed)
                for real_constraint in real_constraints
            ]
            model_benchmarks = self.benchmark_orchestrator.benchmark_graphs(
                [generation.graph for generation in graph_generations]
            )
            all_loss = self.calculate_kl_divergence_loss(
                real_benchmarks=real_benchmarks, model_benchmarks=model_benchmarks
            )
            print(all_loss)
            return all_loss

        benchmark_focus_results = [
            self.optimizers[
                0
            ].find_best_parameters(  # TODO: Make it use all optimizers instead of just the first one
                parameter_bounds=optimizable_model.parameter_bounds,
                all_loss_function=all_loss_function,
                focus_loss_index=focus_loss_index,
                seed=seed,
            )
            for focus_loss_index in track(
                range(len(real_benchmarks)),
                description="Optimizing focus...",
            )
        ]

        return ModelOptimizationResult(benchmark_focus_results=benchmark_focus_results)

    def optimize_null_models_against_real(
        self,
        real_life_model: RealLifeMaps,
        optimizable_models: list[OptimizableModel],
        seed: Optional[Union[int, Generator]] = None,
    ) -> list[ModelOptimizationResult]:
        real_map_generations = real_life_model.get_all_graphs()
        real_constraints = [
            generate_constraints_from_graph(graph_generation.graph)
            for graph_generation in real_map_generations
        ]
        real_benchmarks = self.benchmark_orchestrator.benchmark_graphs(
            [generation.graph for generation in real_map_generations]
        )
        return [
            self.optimize_null_model_against_real(
                real_constraints=real_constraints,
                real_benchmarks=real_benchmarks,
                optimizable_model=optimizable_model,
                seed=seed,
            )
            for optimizable_model in optimizable_models
        ]
