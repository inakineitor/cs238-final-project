from abc import ABC, abstractmethod

from gerrychain import Graph


class Benchmark(ABC):
    @abstractmethod
    def score_graph(self, graph: Graph) -> float:
        pass

    def score_graphs(self, graphs: list[Graph]) -> list[float]:
        return [self.score_graph(graph) for graph in graphs]
