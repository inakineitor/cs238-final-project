from pathlib import Path
import pickle
from typing import Callable
from rich.console import Console
from rich.tree import Tree
from rich.table import Table

from map_analyzer.benchmark_framework.benchmark_orchestrator import (
    BenchmarkOrchestrator,
    BenchmarkOrchestratorResults,
)
from map_analyzer.benchmarks import (
    maximum_degree,
    radius,
    number_of_leaves,
    diameter,
    assortativity,
    average_degree,
    clustering_coefficient,
)  # , face_if_planar
from map_analyzer.models import (
    real_life_maps,
    triangle_edge_deletion,
    flood_fill,
    waxman,
)
from map_analyzer.models.graph_generating_model import GraphGeneratingModel
from map_analyzer.optimization_framework.model_optimization_ochestrator import (
    ModelOptimizationOrchestrator,
    OptimizableModel,
)
from map_analyzer.optimizers import (
    differential_evolution,
    grid_search,
    dual_annealing,
)

NUM_ITERS = 10  # INFO: The higher the number of iterations the more accurate the estimates (set to 50 for comparability because we have 50 state maps)
SEED = 238  # INFO: Seed to ensure reproducible results


def main():
    console = Console()

    console.print("Loading real life models...")
    real_life_model = real_life_maps.RealLifeMaps(
        cache_dir=Path("../data/maps"), map_types=["COUNTY"]
    )  # for sampling real-life maps
    console.print("Real life models loaded", style="green")

    models_to_optimize: list[OptimizableModel] = [
        OptimizableModel(
            "TriangleEdgeDeletionModel_False_False",
            lambda p_delete: triangle_edge_deletion.TriangleEdgeDeletionModel(
                p_delete=p_delete, keep_connected=False, deter=False
            ),
            [(0, 1)],
        ),
        OptimizableModel(
            "TriangleEdgeDeletionModel_False_True",
            lambda p_delete: triangle_edge_deletion.TriangleEdgeDeletionModel(
                p_delete=p_delete, keep_connected=False, deter=True
            ),
            [(0, 1)],
        ),
        OptimizableModel(
            "TriangleEdgeDeletionModel_True_False",
            lambda p_delete: triangle_edge_deletion.TriangleEdgeDeletionModel(
                p_delete=p_delete, keep_connected=True, deter=False
            ),
            [(0, 1)],
        ),
        OptimizableModel(
            "TriangleEdgeDeletionModel_True_True",
            lambda p_delete: triangle_edge_deletion.TriangleEdgeDeletionModel(
                p_delete=p_delete, keep_connected=True, deter=True
            ),
            [(0, 1)],
        ),
        OptimizableModel(
            "WaxmanModel",
            lambda beta, alpha: waxman.WaxmanModel(beta=beta, alpha=alpha),
            [(0, 1), (0, 1)],
        ),
        # flood_fill.FloodFillModel(), # NOTE: FloodFillModel does not have any parameters to optimize
    ]

    optimizers_to_run = [
        grid_search.GridSearchOptimizer(parameter_interval=0.1),
        differential_evolution.DifferentialEvolutionOptimizer(),
        dual_annealing.DualAnnealingOptimizer(),
    ]

    benchmarks_to_run = [
        assortativity.AssortativityBenchmark(),
        average_degree.AverageDegreeBenchmark(),
        clustering_coefficient.ClusteringCoefficientBenchmark(),
        diameter.DiameterBenchmark(),
        maximum_degree.MaximumDegreeBenchmark(),
        number_of_leaves.NumberOfLeavesBenchmark(),
        radius.RadiusBenchmark(),
        # face_if_planar.FaceIfPlanarBenchmark()
    ]

    benchmark_orchestrator = BenchmarkOrchestrator(benchmarks_to_run)
    optimization_orchestrator = ModelOptimizationOrchestrator(
        optimizers_to_run, benchmark_orchestrator
    )

    optimization_results = optimization_orchestrator.optimize_null_models_against_real(
        real_life_model=real_life_model,
        optimizable_models=models_to_optimize,
        seed=SEED,
    )

    with open("optimization_results.pkl", "wb") as outp:
        pickle.dump(optimization_results, outp, pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
    main()
