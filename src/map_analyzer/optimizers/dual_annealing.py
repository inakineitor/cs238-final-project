from typing import Optional, Union
from numpy.random import Generator
from scipy.optimize import dual_annealing

from map_analyzer.optimization_framework.model_parameter_optimizer import (
    FocusLossFunction,
    FocusOptimizationResult,
    ModelParameterOptimizer,
    ParameterBounds,
)


class DualAnnealingOptimizer(ModelParameterOptimizer):
    def find_best_parameters_for_focus_loss(
        self,
        parameter_bounds: ParameterBounds,
        focus_loss: FocusLossFunction,
        seed: Optional[Union[int, Generator]] = None,
    ) -> FocusOptimizationResult:
        optimization_result = dual_annealing(
            func=focus_loss,
            bounds=parameter_bounds,
            callback=(lambda _x, f, _context: print(f"Loss: {f}")),
            seed=seed,
        )
        return FocusOptimizationResult(
            parameters=optimization_result.x, focus_loss=optimization_result.fun
        )
