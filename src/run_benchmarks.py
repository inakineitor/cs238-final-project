from pathlib import Path

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

NUM_ITERS = 10  # INFO: The higher the number of iterations the more accurate the estimates (set to 50 for comparability because we have 50 state maps)
SEED = 238  # INFO: Seed to ensure reproducible results


def main():
    models_to_test = [
        real_life_maps.RealLifeMaps(
            cache_dir=Path("../data/maps"), map_types=["COUNTY"]
        ),  # for sampling real-life maps
        triangle_edge_deletion.TriangleEdgeDeletionModel(),
        flood_fill.FloodFillModel(),
        waxman.WaxmanModel(),
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
        # face_if_planar.FaceIfPlanarBenchmark()
    ]

    orchestrator = BenchmarkOrchestrator(benchmarks_to_run)

    # Collate results
    benchmark_orchestrator_results: list[BenchmarkOrchestratorResults] = []

    # Run real-life benchmark
    num_vertices, graph_nodes = orchestrator.benchmark_model(
        models_to_test[0], NUM_ITERS, SEED
    )
    benchmark_orchestrator_results.append(graph_nodes)

    # Run all other benchmarks
    for i in range(1, len(models_to_test)):
        if i >= 1:  # triangle deletion
            params = {"num_vertices": num_vertices, "p_delete": 0.065, "model": "tri"}
            nvert, graph_nodes = orchestrator.benchmark_model(
                models_to_test[i], NUM_ITERS, SEED, extra_params=params
            )

            print(nvert)
            print(num_vertices)
            benchmark_orchestrator_results.append(graph_nodes)

    # benchmark_orchestrator_results = orchestrator.benchmark_models(
    #     models_to_test, NUM_ITERS, SEED
    # )

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

            benchmark.__class__.print_benchmark_metrics(benchmark_results)


if __name__ == "__main__":
    main()
