from typing import Optional, Union
import numpy as np

from numpy.random import Generator

from map_analyzer.optimization_framework.model_parameter_optimizer import (
    FocusLossFunction,
    FocusOptimizationResult,
    ModelParameterOptimizer,
    ParameterBounds,
)


class GridSearchOptimizer(ModelParameterOptimizer):
    parameter_interval: float

    def __init__(self, parameter_interval: float):
        self.parameter_interval = parameter_interval

    def find_best_parameters_for_focus_loss(
        self,
        parameter_bounds: ParameterBounds,
        focus_loss: FocusLossFunction,
        seed: Optional[Union[int, Generator]] = None,
    ) -> FocusOptimizationResult:
        # Create a grid of parameter combinations based on the bounds and interval
        parameter_grid = self._create_parameter_grid(
            parameter_bounds, self.parameter_interval
        )

        best_parameters = [0.0] * len(parameter_bounds)
        best_focus_loss = float("inf")

        # Iterate over each parameter combination in the grid
        for parameters in parameter_grid:
            focus_loss_value = focus_loss(parameters)
            print(f"Parameters: {parameters}, Loss: {focus_loss_value}")

            if focus_loss_value < best_focus_loss:
                best_parameters = parameters
                best_focus_loss = focus_loss_value

        return FocusOptimizationResult(
            parameters=best_parameters, focus_loss=best_focus_loss
        )

    def _create_parameter_grid(
        self, parameter_bounds: ParameterBounds, interval: float
    ):
        # Create a list of evenly spaced values for each parameter based on the bounds and interval
        parameter_ranges = [
            np.arange(low, high + interval, interval) for low, high in parameter_bounds
        ]

        # Use numpy.meshgrid to generate a grid of parameter combinations
        parameter_grid = np.array(np.meshgrid(*parameter_ranges)).T.reshape(
            -1, len(parameter_bounds)
        )

        return parameter_grid
