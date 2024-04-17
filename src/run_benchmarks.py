from pathlib import Path

from map_analyzer.benchmark_framework.benchmark_orchestrator import (
    BenchmarkOrchestrator,
)
from map_analyzer.benchmarks import maximum_degree, radius, number_of_leaves, diameter, assortativity, average_degree, clustering_coefficient
from map_analyzer.models import real_life_maps, triangle_edge_deletion


NUM_ITERS = (
    50  # INFO: The higher the number of iterations the more accurate the estimates
        # set to 50 for comparability because we have 50 state maps
)
SEED = 238  # INFO: Seed to ensure reproducible results


def main():
    models_to_test = [
        # real_life_maps.RealLifeMaps(Path("../data/maps")), # for sampling real-life maps
        triangle_edge_deletion.TriangleEdgeDeletionModel(probability=0.1, num_pts=1000),
        # TODO: Add more models
    ]

    benchmarks_to_run = [
        assortativity.AssortativityBenchmark(),
        average_degree.AverageDegreeBenchmark(),
        clustering_coefficient.ClusteringCoefficientBenchmark(),
        diameter.DiameterBenchmark(),
        maximum_degree.MaximumDegreeBenchmark(),
        number_of_leaves.NumberOfLeavesBenchmark(),
        radius.RadiusBenchmark(),
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
            
            if benchmark_name in ["RadiusBenchmark", "DiameterBenchmark"]:
                values = [x for x in benchmark_results.all_vals if x != -1] # -1 encodes disconnected graph
                num_disconnected = benchmark_results.all_vals.count(-1)
                print("minimum: ", min(values))
                print("mean: ", sum(values) / len(values))
                print("maximum: ", max(values))
                print(f"Proportion of disconnected graphs: {num_disconnected}/{len(benchmark_results.all_vals)}")
            else:
                for key in ["minimum", "mean", "maximum"]:
                    print(f"{key}: {benchmark_results.__getattribute__(key)}")


if __name__ == "__main__":
    main()
