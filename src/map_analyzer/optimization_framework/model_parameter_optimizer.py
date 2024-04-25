from abc import ABC, abstractmethod
from typing import Callable, Tuple


from map_analyzer.benchmark_framework.benchmark import BenchmarkResults
from map_analyzer.models.graph_generating_model import GraphGeneratingModel


class ModelParameterOptimizer(ABC):
    @abstractmethod
    def find_best_parameters(
        self,
        model: GraphGeneratingModel,
        parameter_bounds: list[Tuple[float, float]],
        loss_function: Callable[[BenchmarkResults], float],
    ) -> float:
        pass
