import networkx as nx

from ..benchmark_framework.benchmark import Benchmark, BenchmarkResults


class RadiusBenchmark(Benchmark):
    def score_graph(self, graph) -> float:
        # Note: radius isn't defined for disconnected graphs
        return nx.radius(graph) if nx.is_connected(graph) else -1

    @classmethod
    def print_benchmark_metrics(cls, benchmark_results: BenchmarkResults):
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
