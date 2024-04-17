from pathlib import Path

from map_analyzer.benchmark_framework.benchmark_orchestrator import (
    BenchmarkOrchestrator,
)
from map_analyzer.benchmarks import maximum_degree, radius, number_of_leaves, diameter, assortativity, average_degree, clustering_coefficient
from map_analyzer.models import real_life_maps, triangle_deletion


NUM_ITERS = (
    10  # INFO: The higher the number of iterations the more accurate the estimates
)
SEED = 238  # INFO: Seed to ensure reproducible results


def main():
    models_to_test = [
        # real_life_maps.RealLifeMaps(Path("../data/maps")),
        triangle_deletion.TriangleDeletionModel(probability=0.1, num_pts=1000),
        # TODO: Add more models
    ]

    benchmarks_to_run = [
        maximum_degree.MaximumDegreeBenchmark(),
        radius.RadiusBenchmark(),
        number_of_leaves.NumberOfLeavesBenchmark(),
        diameter.DiameterBenchmark(),
        assortativity.AssortativityBenchmark(),
        average_degree.AverageDegreeBenchmark(),
        clustering_coefficient.ClusteringCoefficientBenchmark(),
    ]

    orchestrator = BenchmarkOrchestrator(benchmarks_to_run)
    benchmark_orchestrator_results = orchestrator.benchmark_models(
        models_to_test, NUM_ITERS, SEED
    )

    for model, orchestrator_results in zip(
        models_to_test, benchmark_orchestrator_results
    ):
        model_name = model.__class__.__name__
        print(f"========== {model_name} ==========")
        for benchmark, benchmark_results in zip(
            benchmarks_to_run, orchestrator_results.benchmarks
        ):
            benchmark_name = benchmark.__class__.__name__
            print(f"===== {benchmark_name} =====")
            for key in ["minimum", "mean", "maximum"]:
                print(f"{key}: {benchmark_results.__getattribute__(key)}")


if __name__ == "__main__":
    main()
