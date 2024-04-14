from pathlib import Path

from map_analyzer.benchmark_framework.benchmark_orchestrator import (
    BenchmarkOrchestrator,
)
from map_analyzer.benchmarks import maximum_degree, radius, number_of_leaves
from map_analyzer.maps.load_maps import load_all_maps, state_ids, load_map


def main():
    state_names_to_load = ["WA", "MA"]
    # state_names_to_load = list(state_ids.values()) # If you want to load all
    # state_codes_to_load = [state_ids[state_name] for state_name in state_names_to_load]
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
        # TODO: Add more statistics
    ]

    for state_name, state_map in names_state_maps:
        print(state_map)
        print(f"========== {state_name} ==========")
        for benchmark in benchmarks_to_run:
            benchmark_results = benchmark.score_graphs([state_map])
            benchmark_name = benchmark.__class__.__name__
            print(f"===== {benchmark_name} =====")
            print(benchmark_results)
            # for key in ["minimum", "mean", "maximum"]:
            #     print(f"{key}: {benchmark_results.__getattribute__(key)}")

if __name__ == "__main__":
    main()
