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
from map_analyzer.models import real_life_maps, triangle_edge_deletion


NUM_ITERS = (
    10  # INFO: The higher the number of iterations the more accurate the estimates
    # set to 50 for comparability because we have 50 state maps
)
SEED = 238  # INFO: Seed to ensure reproducible results


def main():
    models_to_test = [
        real_life_maps.RealLifeMaps(
            Path("../data/maps")
        ),  # for sampling real-life maps
        triangle_edge_deletion.TriangleEdgeDeletionModel(),
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
        if i == 1:  # triangle deletion
            params = {}
            params["num_vertices"] = num_vertices
            params["p_delete"] = 0.065
            params["model"] = "tri"
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

            if benchmark_name in ["RadiusBenchmark", "DiameterBenchmark"]:
                values = [
                    x for x in benchmark_results.all_vals if x != -1
                ]  # -1 encodes disconnected graph
                num_disconnected = benchmark_results.all_vals.count(-1)
                print("minimum: ", min(values))
                print("mean: ", sum(values) / len(values))
                print("maximum: ", max(values))
                print(
                    f"Proportion of disconnected graphs: {num_disconnected}/{len(benchmark_results.all_vals)}"
                )
            elif benchmark_name == "FaceIfPlanar":
                values = [
                    x for x in benchmark_results.all_vals if x != -1
                ]  # -1 encodes non-planar
                num_nonplanar = benchmark_results.all_vals.count(-1)
                print("minimum: ", min(values))
                print("mean: ", sum(values) / len(values))
                print("maximum: ", max(values))
                print(
                    f"Proportion of non-planar graphs: {num_nonplanar}/{len(benchmark_results.all_vals)}"
                )
            else:
                for key in ["minimum", "mean", "maximum"]:
                    print(f"{key}: {benchmark_results.__getattribute__(key)}")


if __name__ == "__main__":
    main()
