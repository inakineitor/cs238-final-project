from pathlib import Path
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

NUM_ITERS = 10  # INFO: The higher the number of iterations the more accurate the estimates (set to 50 for comparability because we have 50 state maps)
SEED = 238  # INFO: Seed to ensure reproducible results


def main():
    console = Console()

    console.print("Loading real life models...")
    real_life_model = real_life_maps.RealLifeMaps(
        cache_dir=Path("../data/maps"), map_types=["COUNTY"]
    )  # for sampling real-life maps
    console.print("Real life models loaded", style="green")

    models_to_test = [
        triangle_edge_deletion.TriangleEdgeDeletionModel(p_delete=0.065),
        # flood_fill.FloodFillModel(),
        waxman.WaxmanModel(beta=0.4, alpha=0.1),
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

    console.print("Processing benchmark results...")
    benchmark_orchestrator_results = orchestrator.benchmark_null_models_against_real(
        real_life_model=real_life_model,
        models=models_to_test,
        num_iters=NUM_ITERS,
        seed=SEED,
    )
    console.print("Benchmark results processed", style="green")

    for benchmark_orchestrator_result in benchmark_orchestrator_results:
        map_metadata = benchmark_orchestrator_result.real_map_generation.metadata
        real_map_benchmarks = benchmark_orchestrator_result.real_map_benchmarks
        model_benchmarks = benchmark_orchestrator_result.model_benchmarks

        root_style = "bold bright_blue"
        model_style = "bold green"
        benchmark_style = "bold yellow"

        tree = Tree(
            f"==================== [{map_metadata.map_type}] {map_metadata.state_code} ====================",
            style=root_style,
            guide_style=root_style,
        )

        real_life_branch = tree.add(
            "Real Life Map", style=model_style, guide_style=model_style
        )

        for benchmark, benchmark_results in zip(benchmarks_to_run, real_map_benchmarks):
            benchmark_name = benchmark.__class__.__name__
            benchmark_branch = real_life_branch.add(
                benchmark_name, style=benchmark_style, guide_style=benchmark_style
            )
            table = benchmark.__class__.get_table_benchmark_metrics(benchmark_results)
            benchmark_branch.add(table)

        for model, benchmarks in zip(models_to_test, model_benchmarks):
            model_name = model.__class__.__name__
            model_branch = tree.add(
                model_name, style=model_style, guide_style=model_style
            )
            for benchmark, benchmark_results in zip(benchmarks_to_run, benchmarks):
                benchmark_name = benchmark.__class__.__name__
                benchmark_branch = model_branch.add(
                    benchmark_name, style=benchmark_style, guide_style=benchmark_style
                )
                table = benchmark.__class__.get_table_benchmark_metrics(
                    benchmark_results
                )
                benchmark_branch.add(table)

        console.print(tree)


if __name__ == "__main__":
    main()
