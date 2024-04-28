from typing import Optional, Union
from numpy.random import Generator
from scipy.optimize import differential_evolution

from map_analyzer.optimization_framework.model_parameter_optimizer import (
    FocusLossFunction,
    FocusOptimizationResult,
    ModelParameterOptimizer,
    ParameterBounds,
)


class DifferentialEvolutionOptimizer(ModelParameterOptimizer):
    def find_best_parameters_for_focus_loss(
        self,
        parameter_bounds: ParameterBounds,
        focus_loss: FocusLossFunction,
        seed: Optional[Union[int, Generator]] = None,
    ) -> FocusOptimizationResult:
        optimization_result = differential_evolution(
            func=focus_loss,
            bounds=parameter_bounds,
            workers=-1,
            callback=(lambda opt_result: print(f"Loss: {opt_result.fun}")),
            seed=seed,
        )
        return FocusOptimizationResult(
            parameters=optimization_result.x, focus_loss=optimization_result.fun
        )
