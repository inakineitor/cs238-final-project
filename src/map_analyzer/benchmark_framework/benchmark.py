from abc import ABC, abstractmethod
from dataclasses import dataclass

import numpy as np
from gerrychain import Graph


@dataclass
class BenchmarkResults:
    minimum: float
    mean: float
    maximum: float
    all_vals: list[float]


class Benchmark(ABC):
    @abstractmethod
    def score_graph(self, graph: Graph) -> float:
        pass

    def score_graphs(self, graphs: list[Graph]) -> list[float]:
        return [self.score_graph(graph) for graph in graphs]

    def benchmark_graphs(self, graphs: list[Graph]) -> BenchmarkResults:
        scores = self.score_graphs(graphs)
        return BenchmarkResults(
            minimum=np.min(scores),
            mean=float(np.mean(scores)),
            maximum=np.max(scores),
            all_vals=scores,
        )

    @classmethod
    def print_benchmark_metrics(cls, benchmark_results: BenchmarkResults):
        for key in ["minimum", "mean", "maximum"]:
            print(f"{key}: {benchmark_results.__getattribute__(key)}")
