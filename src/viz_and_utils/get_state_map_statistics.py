from pathlib import Path

from map_analyzer.benchmark_framework.benchmark_orchestrator import (
    BenchmarkOrchestrator,
)
from map_analyzer.benchmarks import (
    maximum_degree,
    radius,
    number_of_leaves,
    diameter,
    assortativity,
    average_degree,
    clustering_coefficient,
)
from map_analyzer.maps.load_maps import load_all_maps, state_ids, load_map
from collections import defaultdict
import json


def main():
    # state_names_to_load = ["WA", "MA"] # if you want to load specific states only
    state_names_to_load = list(state_ids.keys())  # If you want to load all
    # map types are ["BLOCK", "BG", "TRACT", "COUSUB", "COUNTY"]
    map_type = "TRACT"
    loaded_maps = [
        load_map(state_code, map_type, Path("../data/maps"))
        for state_code in state_names_to_load
    ]
    names_state_maps = zip(state_names_to_load, loaded_maps)

    benchmarks_to_run = [
        maximum_degree.MaximumDegreeBenchmark(),
        radius.RadiusBenchmark(),
        number_of_leaves.NumberOfLeavesBenchmark(),
        diameter.DiameterBenchmark(),
        assortativity.AssortativityBenchmark(),
        average_degree.AverageDegreeBenchmark(),
        clustering_coefficient.ClusteringCoefficientBenchmark(),
    ]

    overall_results = defaultdict(list)
    for state_name, state_map in names_state_maps:
        print(state_map)
        print(f"========== {state_name} ==========")
        for benchmark in benchmarks_to_run:
            benchmark_results = benchmark.score_graphs([state_map])
            benchmark_name = benchmark.__class__.__name__
            print(f"===== {benchmark_name} =====")
            print(benchmark_results)
            overall_results[benchmark_name].append(
                benchmark_results[0]
            )  # these benchmarks all generate one number per graph

    with open(f"do_not_commit/{map_type}_main_stats.json", "w") as fp:
        json.dump(overall_results, fp)
        print("dictionary saved successfully to file")


if __name__ == "__main__":
    main()
