from ..benchmark_framework.benchmark import Benchmark


class NumberOfLeavesBenchmark(Benchmark):
    def score_graph(self, graph) -> float:
        return len(
            [x for x in graph.nodes() if graph.degree[x] == 1]
        )  # TODO: Check that definition of leaf is correct (Daryl did not define it in the email)
