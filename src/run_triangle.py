from pathlib import Path
from rich.console import Console
from rich.tree import Tree
from rich.table import Table
import pickle
import random
import pandas as pd

from map_analyzer.benchmark_framework.benchmark_orchestrator_rhea import (
    BenchmarkOrchestrator,
    BenchmarkOrchestratorResults,
    ModelConstraints
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
    # flood_fill,
    # waxman
)

NUM_ITERS = 1  # INFO: The higher the number of iterations the more accurate the estimates (set to 50 for comparability because we have 50 state maps)
SEED = 238  # INFO: Seed to ensure reproducible results


def main():
    console = Console()

    console.print("Loading real life models...")
    real_life_model = real_life_maps.RealLifeMaps(
        cache_dir=Path("../data/maps"), map_types=["TRACT"]
    )  # for sampling real-life maps
    console.print("Real life models loaded", style="green")

    models_to_test = [
        triangle_edge_deletion.TriangleEdgeDeletionModel(p_delete=0.065, keep_connected=False, deter=False),
        triangle_edge_deletion.TriangleEdgeDeletionModel(p_delete=0.065, keep_connected=True, deter=False),
        triangle_edge_deletion.TriangleEdgeDeletionModel(p_delete=0.065, keep_connected=True, deter=True),
        triangle_edge_deletion.TriangleEdgeDeletionModel(p_delete=0.065, keep_connected=False, deter=True),
        # flood_fill.FloodFillModel(),
        # waxman.WaxmanModel(beta=0.4, alpha=0.1),
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

    results = []

    for benchmark_orchestrator_result in benchmark_orchestrator_results:
        map_metadata = benchmark_orchestrator_result.real_map_generation.metadata
        real_map_benchmarks = benchmark_orchestrator_result.real_map_benchmarks
        model_benchmarks = benchmark_orchestrator_result.model_benchmarks

        

        root_style = "bold bright_blue"
        real_life_style = "bold yellow"
        model_style = "bold green"
        benchmark_style = "bold green"

        tree = Tree(
            f"==================== [{map_metadata.map_type}] {map_metadata.state_code} ====================",
            style=root_style,
            guide_style=root_style,
        )

        real_life_branch = tree.add(
            "Real Life Map", style=real_life_style, guide_style=real_life_style
        )

        real_life_table = Table()
        for benchmark, benchmark_results in zip(benchmarks_to_run, real_map_benchmarks):
            benchmark_name = benchmark.__class__.__name__
            benchmark.__class__.add_benchmark_metrics_to_table(
                real_life_table, benchmark_name, benchmark_results
            )
        real_life_branch.add(real_life_table)

        for model, benchmarks in zip(models_to_test, model_benchmarks):
            model_name = model.__class__.__name__
            model_branch = tree.add(
                model_name, style=model_style, guide_style=model_style
            )
            model_table = Table()
            for benchmark, benchmark_results in zip(benchmarks_to_run, benchmarks):
                benchmark_name = benchmark.__class__.__name__
                benchmark.__class__.add_benchmark_metrics_to_table(
                    model_table, benchmark_name, benchmark_results
                )
                # print("TESTING TESTING")
                # print(model_name)
                # print(benchmark_name)
                # print(benchmark_results)
                # print(benchmark_results.minimum)
                row = {"state": map_metadata.state_code,
                        "model": model_name,
                       "benchmark": benchmark_name,
                       "min": benchmark_results.minimum,
                       "mean": benchmark_results.mean,
                       "max":benchmark_results.maximum
                       }
                results.append(row)
            model_branch.add(model_table)
        console.print(tree)
    df = pd.DataFrame(results)
    df.to_csv("out.csv")    
        


if __name__ == "__main__":
    main()
