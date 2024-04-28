from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Optional, Union

from numpy.random import Generator


@dataclass
class FocusOptimizationResult:
    parameters: list[float]
    focus_loss: float


@dataclass
class AllOptimizationResult:
    parameters: list[float]
    all_loss: list[float]
    focus_index: int


ParameterBounds = list[tuple[float, float]]
FocusLossFunction = Callable[..., float]
AllLossFunction = Callable[..., list[float]]


class ModelParameterOptimizer(ABC):
    @abstractmethod
    def find_best_parameters_for_focus_loss(
        self,
        parameter_bounds: ParameterBounds,
        focus_loss: FocusLossFunction,
        seed: Optional[Union[int, Generator]] = None,
    ) -> FocusOptimizationResult:
        pass

    def find_best_parameters(
        self,
        parameter_bounds: ParameterBounds,
        all_loss_function: AllLossFunction,
        focus_loss_index: int,
        seed: Optional[Union[int, Generator]] = None,
    ) -> AllOptimizationResult:
        def focus_loss_function(*args):
            return all_loss_function(*args)[focus_loss_index]

        focus_optimization_result = self.find_best_parameters_for_focus_loss(
            parameter_bounds=parameter_bounds,
            focus_loss=focus_loss_function,
            seed=seed,
        )
        all_loss = all_loss_function(*focus_optimization_result.parameters)
        return AllOptimizationResult(
            parameters=focus_optimization_result.parameters,
            all_loss=all_loss,
            focus_index=focus_loss_index,
        )
